use pyo3::prelude::*;

extern crate image;

use image::{GenericImageView, imageops};

#[pyfunction]
fn grayscale(img: &str, filename: &str) -> PyResult<bool> {
    let img = image::open(img).unwrap();
    let grey = img.grayscale();
    grey.save(filename).unwrap();
    Ok(true)
}

#[pyfunction]
fn blur(img: &str, filename: &str, sigma: f32) -> PyResult<bool> {
    let img = image::open(img).unwrap();
    let blurred_img = img.blur(sigma);
    blurred_img.save(filename).unwrap();
    Ok(true)
}

#[pyfunction]
fn brighten(img: &str, filename: &str, value: i32) -> PyResult<bool> {
    let img = image::open(img).unwrap();
    let brightened_img = img.brighten(value);
    brightened_img.save(filename).unwrap();
    Ok(true)
}

#[pyfunction]
fn flip_horizontal(img: &str, filename: &str) -> PyResult<bool> {
    let mut img = image::open(img).unwrap();
    let flipped_img = imageops::flip_horizontal(&mut img);
    flipped_img.save(filename).unwrap();
    Ok(true)
}

#[pyfunction]
fn flip_vertical(img: &str, filename: &str) -> PyResult<bool> {
    let mut img = image::open(img).unwrap();
    let flipped_img = imageops::flip_vertical(&mut img);
    flipped_img.save(filename).unwrap();
    Ok(true)
}

#[pyfunction]
fn crop(img: &str, filename: &str, x: u32, y: u32, width: u32, height: u32) -> PyResult<bool> {
    let mut img = image::open(img).unwrap();
    let cropped_img = img.crop(x, y, width, height);
    cropped_img.save(filename).unwrap();
    Ok(true)
}

#[pymodule]
fn filters(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(grayscale, m)?)?;
    m.add_function(wrap_pyfunction!(blur, m)?)?;
    m.add_function(wrap_pyfunction!(brighten, m)?)?;
    m.add_function(wrap_pyfunction!(flip_horizontal, m)?)?;
    m.add_function(wrap_pyfunction!(flip_vertical, m)?)?;
    m.add_function(wrap_pyfunction!(crop, m)?)?;
    Ok(())
}
