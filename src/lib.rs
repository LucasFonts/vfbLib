use pyo3::prelude::*;
use std::io::prelude::*;
use std::io::BufReader;
use std::fs::File;


// internal functions

fn read_encoded_value<R>(r: &mut BufReader<R>) -> i32 where R: std::io::Read {
    let mut value = [0; 1];
    r.read_exact(&mut value[..]).expect("ValueError");
    let val = value[0];
    if val < 0x20 {
        return 0;
    } else if val < 0xF7 {
        return (val - 0x8B).into();
    } else if val <= 0xFA {
        let mut value2 = [0; 1];
        r.read_exact(&mut value2[..]).expect("ValueError");
        let val2 = value2[0];
        return (val - 0x8B + (val - 0xF7) * 0xFF + val2).into();
    } else if val <= 0xFE {
        let mut value2 = [0; 1];
        r.read_exact(&mut value2[..]).expect("ValueError");
        let val2 = value2[0];
        return (0x8F - val - (val - 0xFB) * 0xFF - val2).into();
    } else if val == 0xFF {
        let mut value2 = [0; 4];
        r.read_exact(&mut value2[..]).expect("ValueError");
        // FIXME: Add values
        let val2 = value2[0];
        return val2.into();
    } else {
        return 0;
    }
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
    let mut filetyp = [0; 5];
    let mut header1 = [0; 2];
    let mut header2 = [0; 2];
    let mut reserve = [0; 34];
    let mut header3 = [0; 2];
    let mut header4 = [0; 2];
    let mut header5 = [0; 2];
    let mut header6 = [0; 2];
    let mut header7 = [0; 2];
    let mut header8 = [0; 2];

    r.read_exact(&mut header0[..])?;
    r.read_exact(&mut filetyp[..])?;
    r.read_exact(&mut header1[..])?;
    r.read_exact(&mut header2[..])?;
    r.read_exact(&mut reserve[..])?;
    r.read_exact(&mut header3[..])?;
    r.read_exact(&mut header4[..])?;
    r.read_exact(&mut header5[..])?;
    r.read_exact(&mut header6[..])?;
    r.read_exact(&mut header7[..])?;
    r.read_exact(&mut header8[..])?;

    // println!("{:#?}", filetype);

    // Read 3 key/value pairs (?)
    let mut _k = [0; 1];
    let mut _v: i32 = -1;
    for _i in 9..=11 {
        r.read_exact(&mut _k[..])?;
        _v = read_encoded_value(&mut r);
        println!("{:#?}", _k[0]);
        println!("{:#?}", _v);
    }

    let mut header9 = [0; 2];
    let mut headera = [0; 2];

    r.read_exact(&mut header9[..])?;
    r.read_exact(&mut headera[..])?;

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
