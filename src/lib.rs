use pyo3::prelude::*;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;


// internal functions

fn read_encoded_value<R>(r: &BufReader<R>) -> i32 {
    return 0;
}

// struct VfbHeader {

// }

struct VfbField<'a> {
    key: u16,
    size: u16,
    data: Vec<&'a [u8]>,
}


struct VfbObject<'a> {
    // header: &VfbHeader,
    fields: Vec<VfbField<'a>>,
}

// fn read_header(buf_reader: std::io::BufReader<R>) {
//     // pass
// }


// functions exposed to Python

/// Reads the basic structure of the VFB into a struct.
#[pyfunction]
fn read_vfb(path: &str) -> PyResult<()> {
    let file = File::open(path)?;
    let mut r = BufReader::new(file);

    let mut header0 = [0; 1];
    let mut filetype = [0; 5];
    let mut header1 = [0; 2];
    let mut header2 = [0; 2];
    let mut reserved = [0; 34];
    let mut header3 = [0; 2];
    let mut header4 = [0; 2];
    let mut header5 = [0; 2];
    let mut header6 = [0; 2];
    let mut header7 = [0; 2];
    let mut header8 = [0; 2];

    r.read_exact(&mut header0[..])?;
    r.read_exact(&mut filetype[..])?;
    r.read_exact(&mut header1[..])?;
    r.read_exact(&mut header2[..])?;
    r.read_exact(&mut reserved[..])?;
    r.read_exact(&mut header3[..])?;
    r.read_exact(&mut header4[..])?;
    r.read_exact(&mut header5[..])?;
    r.read_exact(&mut header6[..])?;
    r.read_exact(&mut header7[..])?;
    r.read_exact(&mut header8[..])?;

    println!("{:#?}", filetype);

    // Read 3 key/value pairs (?)
    let mut _k = [0; 1];
    let mut _v: i32 = -1;
    for _i in 9..=11 {
        r.read_exact(&mut _k[..])?;
        _v = read_encoded_value(&r);
    }

    // let mut obj = ...
    let _obj = VfbObject {
        fields: Vec::new(),
    };
    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn vfbreader(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_vfb, m)?)?;
    Ok(())
}
