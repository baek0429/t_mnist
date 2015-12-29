// canvas
'use strict';
function Canvas(id,width,height){
    this.canvas = document.getElementById(id);
    this.ctx = $('#'+id)[0].getContext("2d");
    this.size = width;
}

Canvas.prototype.setEvent = function(){
    var that = this;
    this.ctx.fillStyle = '#FFFFFF';
    this.ctx.fillRect(0, 0, 500, 500);
    that.canvas.addEventListener("mousemove", function(e){
        if(that.isDrawing){
            that.ctx.lineWidth = 16;
            that.ctx.lineCap = 'round';
            var newXY = that.getMousePos(that.canvas,e);

            $('#coord').html("("+parseInt(newXY[0])+", "+newXY[1]+")");
            var curr = [parseInt(newXY[0]),parseInt(newXY[1])];
            that.ctx.beginPath();
            that.ctx.moveTo(that.prev[0], that.prev[1]);
            that.ctx.lineTo(curr[0], curr[1]);
            that.ctx.stroke();
            that.ctx.closePath();
            that.prev = curr;
        }
    });
    that.canvas.addEventListener("mousedown", function(e){
        that.canvas.style.cursor = 'default';
        var newXY = that.getMousePos(that.canvas,e);
        that.prev = [parseInt(newXY[0]),newXY[1]];
        that.isDrawing = true;
    });
    that.canvas.addEventListener("mouseup", function(e){
        that.isDrawing = false;
        var img = new Image();
        that.ctx2= $('#smallcanvas')[0].getContext("2d");
        img.onload = (function(){
            var inputs= [];
            that.ctx2.drawImage(img,0,0,img.width,img.height,0,0,28,28);

            var data = that.ctx2.getImageData(0,0,28,28).data; // 255*28
            for(var i = 0;i<28;i++){
                for(var j=0;j<28;j++){
                    var n = 4 * (i * 28 + j); // get rgb first three 
                    inputs[i*28+j] = (data[n+0] + data[n+1] + data[n+2])/3; //28by28
                    that.ctx2.fillStyle = 'rgb(' + [data[n + 0], data[n + 1], data[n + 2]].join(',') + ')'; //fourth zero
                    that.ctx2.fillRect(j*5,i*5,5,5);
                }
            }
            // all white.
            if (Math.min(...inputs) === 255) {
                return;
            }

            $.ajax({
                url: '/main',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(inputs),
                success: function(val){
                    console.log(val);
                },
            });
        });
    img.src = that.canvas.toDataURL();
    })
}

Canvas.prototype.getMousePos = function(c ,evt) {
    $('#coord2').html("("+evt.clientX+", "+evt.clientY+")");
    var rect = c.getBoundingClientRect();
    return [evt.clientX - rect.left,
    evt.clientY - rect.top];
}

// inititate canvases
function initiate(){
    var canvas = new Canvas("canvas",500,500);
    canvas.setEvent();
}

$(function(){
    initiate();
    console.log("initated");
    $('#clear').click(() =>{
        initiate();
    });
});