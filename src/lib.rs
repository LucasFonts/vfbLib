use pyo3::prelude::*;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

// struct VfbHeader {

// }

struct VfbField {
    //  VfbField<'a>
    key: u16,
    // offset: u64,
    size: u32,
    // data: Vec<&'a [u8]>,
}

struct VfbObject {
    //  VfbObject<'a>
    // header: &VfbHeader,
    fields: Vec<VfbField>,
}

// internal functions

fn read_encoded_value<R>(r: &mut BufReader<R>) -> i32
where
    R: std::io::Read,
{
    let result: i32;
    let mut value = [0u8; std::mem::size_of::<u8>()];
    r.read_exact(&mut value).expect("ValueError");
    let val = value[0];
    if val < 0x20 {
        return 0; // FIXME
    } else if val < 0xF7 {
        result = (val - 0x8B).into();
    } else if val < 0xFF {
        let mut value2 = [0u8; std::mem::size_of::<u8>()];
        r.read_exact(&mut value2).expect("ValueError");
        let val2 = value2[0];
        if val < 0xFB {
            result = (val - 0x8B + (val - 0xF7) * 0xFF + val2).into();
        } else {
            // Negative number
            result = (0x8F - val - (val - 0xFB) * 0xFF - val2).into();
        }
    } else if val == 0xFF {
        let mut value2 = [0u8; std::mem::size_of::<i32>()];
        r.read_exact(&mut value2).expect("ValueError");
        result = i32::from_be_bytes(value2);
    } else {
        // Can't happen
        result = 0; // FIXME
    }
    println!("Raw: {}, result: {}", val, result);
    return result;
}

fn read_entry<R>(r: &mut BufReader<R>) -> VfbField
where
    R: std::io::Read,
    R: Seek,
{
    // let offset: u64 = r.stream_position();
    let mut key = [0u8, 2];
    r.read_exact(&mut key);
    let finalkey = u16::from_le_bytes(key);

    let finalsize: u32;
    if finalkey & 0x8000 > 0 {
        let mut size = [0u8, 2];
        r.read_exact(&mut size);
        finalsize = size[0].into();
    } else {
        let mut size = [0u8, 2];
        r.read_exact(&mut size);
        finalsize = size[0].into();
    }
    r.seek_relative(finalsize.into());
    // let mut data: Vec<u8> = Vec::with_capacity(finalsize.try_into().unwrap());
    // r.read_exact(&mut data);
    // println!("{:#?}", data);

    return VfbField {
        key: finalkey,
        // offset: offset,
        size: finalsize,
        // data: data,
    };
}

fn read_header<R>(r: &mut BufReader<R>)
where
    R: std::io::Read,
{
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

    r.read_exact(&mut header0[..]);
    r.read_exact(&mut filetyp[..]);
    r.read_exact(&mut header1[..]);
    r.read_exact(&mut header2[..]);
    r.read_exact(&mut reserve[..]);
    r.read_exact(&mut header3[..]);
    r.read_exact(&mut header4[..]);
    r.read_exact(&mut header5[..]);
    r.read_exact(&mut header6[..]);
    r.read_exact(&mut header7[..]);
    r.read_exact(&mut header8[..]);

    // println!("{:#?}", filetype);

    // Read 3 key/value pairs (?)
    let mut _k = [0; 1];
    let mut _v: i32 = -1;
    for _i in 9..=11 {
        r.read_exact(&mut _k[..]);
        _v = read_encoded_value(r);
        println!("{:#?}: {:#?}", _k[0], _v);
    }

    let mut header9 = [0; 1];
    let mut headera = [0; 2];
    let mut headerb = [0; 2];

    r.read_exact(&mut header9[..]);
    r.read_exact(&mut headera[..]);
    r.read_exact(&mut headerb[..]);
}

// functions exposed to Python

/// Reads the basic structure of the VFB into a struct.
#[pyfunction]
fn read_vfb(path: &str) -> PyResult<()> {
    let file = File::open(path).expect("Failed to open file");
    let mut r = BufReader::new(file);

    read_header(&mut r);

    let mut obj = VfbObject { fields: Vec::new() };
    let mut field: VfbField;
    let mut i = 0;
    loop {
        // use std::io::ErrorKind;
        field = read_entry(&mut r);
        println!("{}: {}", field.key, field.size);
        obj.fields.append(&mut vec![field]);
        // Err(error) if error.kind() == ErrorKind::UnexpectedEof => break;
        // _ => {}
        i += 1;
        if i > 262 {
            break;
        }
    }
    Ok(())
}

/// A Python module implemented in Rust.
#[pymodule]
fn vfbreader(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_vfb, m)?)?;
    Ok(())
}
