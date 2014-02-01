var modelPath = null;

/**
 *  Success callback for the call to ShapeJS
 */
function onGenerateModelSuccess(aoptOutput, modelFilePath) {
    // grab the iframe using the path to the aopt file
    aoptOutput = 'https://images.shapeways.com/3dviewer/aopt-file?aoptFilePath=' + aoptOutput + "&width=500&height=300";
    $("#x3d-iframe").attr('src', aoptOutput);

    // set the model path for uploading later
    modelPath = modelFilePath;
}

/**
 * Uploads a model with the Shapeways API.
 */
function uploadModel() {
    $.post('/upload',{
        modelFilePath: modelPath, modelFileName: "ShapeJSDemoModel.x3db"
    }, function(response) {
        // now that we have a model id, we can create a link to the model on shapeways
        var decodedResponse = JSON.parse(response);
        var modelId = decodedResponse.modelId;
        var modelLink = $('#model-link');
        modelLink.html('<a href="https://www.shapeways.com/model/upload-and-buy/' + modelId + '" target="_blank">Click here to see your model on shapeways.com!</a>');
        modelLink.css('display', 'block');
    });
}