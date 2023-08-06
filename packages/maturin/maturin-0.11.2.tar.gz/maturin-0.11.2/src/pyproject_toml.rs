use anyhow::{format_err, Context, Result};
use pyproject_toml::PyProjectToml as ProjectToml;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

/// The `[tool]` section of a pyproject.toml
#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(rename_all = "kebab-case")]
pub struct Tool {
    maturin: Option<ToolMaturin>,
}

/// The `[tool.maturin]` section of a pyproject.toml
#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(rename_all = "kebab-case")]
pub struct ToolMaturin {
    sdist_include: Option<Vec<String>>,
}

/// A pyproject.toml as specified in PEP 517
#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(rename_all = "kebab-case")]
pub struct PyProjectToml {
    #[serde(flatten)]
    inner: ProjectToml,
    /// PEP 518: The `[tool]` table is where any tool related to your Python project, not just build
    /// tools, can have users specify configuration data as long as they use a sub-table within
    /// `[tool]`, e.g. the flit tool would store its configuration in `[tool.flit]`.
    ///
    /// We use it for `[tool.maturin]`
    pub tool: Option<Tool>,
}

impl std::ops::Deref for PyProjectToml {
    type Target = ProjectToml;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

impl PyProjectToml {
    /// Returns the contents of a pyproject.toml with a `[build-system]` entry or an error
    ///
    /// Does no specific error handling because it's only used to check whether or not to build
    /// source distributions
    pub fn new(project_root: impl AsRef<Path>) -> Result<PyProjectToml> {
        let path = project_root.as_ref().join("pyproject.toml");
        let contents = fs::read_to_string(&path).context(format!(
            "Couldn't find pyproject.toml at {}",
            path.display()
        ))?;
        let pyproject: PyProjectToml = toml::from_str(&contents)
            .map_err(|err| format_err!("pyproject.toml is not PEP 517 compliant: {}", err))?;
        pyproject.warn_missing_maturin_version();
        Ok(pyproject)
    }

    /// Returns the value of `[maturin.sdist-include]` in pyproject.toml
    pub fn sdist_include(&self) -> Option<&Vec<String>> {
        self.tool.as_ref()?.maturin.as_ref()?.sdist_include.as_ref()
    }

    /// Having a pyproject.toml without a version constraint is a bad idea
    /// because at some point we'll have to do breaking changes and then source
    /// distributions would break
    ///
    /// Returns true if the pyproject.toml has the constraint
    pub fn warn_missing_maturin_version(&self) -> bool {
        let maturin = env!("CARGO_PKG_NAME");
        if let Some(requires_maturin) = self
            .build_system
            .requires
            .iter()
            .find(|x| x.starts_with(maturin))
        {
            // Note: Update this once 1.0 is out
            assert_eq!(env!("CARGO_PKG_VERSION_MAJOR"), "0");
            let current_minor: usize = env!("CARGO_PKG_VERSION_MINOR").parse().unwrap();
            if requires_maturin == maturin {
                eprintln!(
                    "⚠  Warning: Please use {maturin} in pyproject.toml with a version constraint, \
                    e.g. `requires = [\"{maturin}>=0.{current},<0.{next}\"]`. \
                    This will become an error.",
                    maturin = maturin,
                    current = current_minor,
                    next = current_minor + 1,
                );
                return false;
            }
        }
        true
    }
}

#[cfg(test)]
mod tests {
    use crate::PyProjectToml;
    use fs_err as fs;
    use tempfile::TempDir;

    #[test]
    fn test_warn_missing_maturin_version() {
        let with_constraint = PyProjectToml::new("test-crates/pyo3-pure").unwrap();
        assert!(with_constraint.warn_missing_maturin_version());
        let without_constraint_dir = TempDir::new().unwrap();

        fs::write(
            without_constraint_dir.path().join("pyproject.toml"),
            r#"[build-system]
            requires = ["maturin"]
            build-backend = "maturin""#,
        )
        .unwrap();
        let without_constraint = PyProjectToml::new(without_constraint_dir).unwrap();
        assert!(!without_constraint.warn_missing_maturin_version());
    }
}
