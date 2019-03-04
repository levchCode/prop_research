let data_URL = "https://dl.dropboxusercontent.com/s/edhaj1h8jk6pfin/data.csv?dl=0";
let data;
let model;
let iter = 200

function preload(){
    noLoop()
    data = loadTable(data_URL, "csv", "header")
}


async function setup() {
    len = data.getRowCount();
    let a_arr = [];
    let k_arr = [];
    let solar_flux_arr = [];
    let vol_arr = [];

    for (let i = 0; i < len; i++)
    {
        a_arr.push(data.getNum(i, "a"))
        k_arr.push(data.getNum(i, "k"))
        solar_flux_arr.push(data.getNum(i, "solar_flux"))
        vol_arr.push(data.getNum(i, "volume"))
    }

    const x = tf.tensor2d([a_arr, k_arr, solar_flux_arr]).reshape([len, 3])
    const y = tf.tensor1d(vol_arr)
    
    model = tf.sequential()
    const hidden = tf.layers.dense({inputShape:[3], units:50, activation: "relu"});
    const output = tf.layers.dense({units:1, activation: "relu"});
    model.add(hidden)
    model.add(output)

    model.compile({optimizer:tf.train.adam(0.015), loss:"meanSquaredError"})
    
    for (let i = 0; i < iter; i++)
    {
        const h = await model.fit(x, y, {epochs:1})
        document.getElementById("t_p").innerHTML = h.history.loss[0]
        
    }
    //document.getElementById("t_p").innerHTML = "DONE!"

}


async function predict()
{
   let k = parseInt(document.getElementById("k").value)
   let a = parseInt(document.getElementById("a").value)
   let sf = parseInt(document.getElementById("sf").value)

    const inputs = tf.tensor2d([[a, k, sf]])
    const out = await model.predict(inputs).data()
    document.getElementById("volume").innerHTML = out
}
