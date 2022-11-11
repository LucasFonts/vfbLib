use pyo3::prelude::*;
use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;


// internal functions

struct VfbHeader {

}

struct VfbField {
    key: u16,
    data: Vec<bytes>,
}


struct VfbObject {
    header: &VfbHeader,
    fields: Vec<VfbField>,
}


// functions exposed to Python

#[pyfunction]
fn read_vfb_from_path(vfb_path: Vec<str>) -> PyResult<VfbObject> {
    let mut file = File::open(vfb_path)?;
    let mut buf_reader = BufReader::new(file);
    // let font_object = Vec;
    // Ok(font_object)
    Ok(())
}


// The Python module

#[pymodule]
fn vfbreader(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_vfb_from_path, m)?)?;
    Ok(())
}
