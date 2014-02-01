var creator = "VolumeSculptor";

/**
 * Send a script to the ShapeJS pipeline.
 *
 * @param string code - the ShapeJS script
 * @param string formName - the form that contains the ShapeJS arguments
 * @param function successCallback - a callback function that will be given
 * the aopt file path (for preview) and model file path (for upload)
 */
function getShapeJsPreview(code, formName, successCallback, generate2dRender, endPoint) {
    var pipeline = "VolumeSculptorProcessing";
    var generateImage = 'false';

    if(generate2dRender) {
        generateImage = 'true';
    }

    var params = {
        'persistent': 'false',
        'pipeline': pipeline,
        'action': 'preview',
        'accuracy': 'VISUAL',
        'previewQuality': 'LOW',
        'regions': 'ONE', // ['ALL', 'ONE'] number of regins to keep
        'visRemovedRegions': 'false',
        'optimizeX3D': 'true',
        'script': code,
        'generateImage': generateImage
    }

    successCall = function(jsonObj) {
        var returnMap = processShapeJsPreviewSuccess(jsonObj);
        if(successCallback) {
            var aoptOutput = returnMap.aoptOutput;
            var modelFilePath = returnMap.modelFilePath;
            var renderImageOutput = returnMap.thumbnailOutput;

            successCallback(aoptOutput, modelFilePath, renderImageOutput);
        }
    }

    /**
     * To get around cross domain issues, we need to proxy the request to
     * the actual ShapeJS server
     */
    options = {
        url: endPoint || "http://www.shapeways.com/creator/exec_pipeline_proxy",
        type: 'post',
        timeout: 180000,
        datatype: 'json',
        data: params,
        success:successCall,
        error: processShapeJsPreviewFailure
    };

    jQuery('#' + formName).ajaxSubmit(options);
}

function processShapeJsPreviewSuccess(jsonObj) {
    var stateMap = jsonObj.state;
    var aoptOutput = null;
    if (jsonObj.result == "SUCCESS") {
        aoptOutput = stateMap['Aopt.output'];

        var creatorOutput = stateMap[creator + '.output'];

        if (aoptOutput == undefined || aoptOutput == null) {
            aoptOutput = creatorOutput;
        } else {
            for(var i=0; aoptOutput.length; i++) {
                if (aoptOutput[i].indexOf('.x3d', aoptOutput[i].length - 4) !== -1) {
                    aoptOutput = aoptOutput[i];
                    break;
                }
            }
        }
    }
    else {
        var reason = "Unknown";

        if (stateMap != undefined) {
            reason = stateMap[creator + '.runtimeError'];
            console.log("ShapeJS ERROR Debug print: " + stateMap[creator + '.debugPrint']);
            console.log("ShapeJS ERROR Reason: " + reason);
        }
    }

    return {aoptOutput: aoptOutput, modelFilePath: creatorOutput, thumbnailOutput: stateMap['Thumbnail.output']};
}

function processShapeJsPreviewFailure(data) {
    console.log("ERROR from exec pipeline.");
}