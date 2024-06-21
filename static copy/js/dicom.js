// $(document).ready(function(){
//     const image = $('#chartImg')[0];
//     if (image.complete) {
//         imageLoaded();
//     } else {
//         // If not loaded, attach a load event handler
//         image.onload = imageLoaded;
//     }
//     function imageLoaded() {
//         result_dict = dicomResult.result_dict
//         result_dict_key = Object.keys(result_dict)
//         console.log(result_dict)
//         const canvas = document.getElementById('lineCanvas');
//         const ctx = canvas.getContext('2d');
//         const x_coords = [];
//         Object.keys(result_dict).forEach(function(image_x) {
//             x_coords.push(image_x);
//         });
//         const min_x = x_coords[0];
//         const max_x = x_coords[x_coords.length - 1];
        
//         // 1. Adım: Resmin genişliğini 3'e böl
//         const newImageWidth = max_x - min_x;

//         // 2. Adım: Canvas genişliğini ve yüksekliğini ayarla
//         const image_natural_width = image.naturalWidth;
//         const resulation_rate = image.width / image_natural_width;
//         canvas.width = (newImageWidth+2)*resulation_rate;
//         canvas.height = image.height;
//         canvas.style.left = `${(min_x)*resulation_rate}px`
//         // 3. Adım: Çizgileri yeni canvas genişliğine göre çiz

//         const lineCount = x_coords.length;
//         const lineWidth = 0.00001;
//         const startOffset = 0;
//         const lineSpacing = newImageWidth/lineCount;

//         for (let i = 0; i < lineCount; i++) {
//             const x = (x_coords[i]-min_x) * resulation_rate
//             ctx.strokeStyle = '#6D95FF'; // Örnek orijinal renk
//             ctx.beginPath();
//             ctx.moveTo(x, 0);
//             ctx.lineTo(x, canvas.height);
//             ctx.stroke();
//         }

//         // Canvas üzerinde tıklama olayını dinle
//         canvas.addEventListener('click', function (event) {
//             const mouseX = event.clientX - canvas.getBoundingClientRect().left;
//             const mouseY = event.clientY - canvas.getBoundingClientRect().top;
        
//             // Hangi çizgi üzerinde olduğunu bul
//             const lineIndex = parseInt((mouseX - startOffset) / ((lineWidth + lineSpacing)*resulation_rate));
        
//             let slice_path = result_dict[result_dict_key[lineIndex]].path
//             $('#mini-slice').attr("src", slice_path)
            
//             console.log(`Çizgi ${lineIndex + 1} üzerine tıklandı.`);
//         });


//         canvas.addEventListener('mousemove', function (event) {
//             const mouseX = event.clientX - canvas.getBoundingClientRect().left;
//             const mouseY = event.clientY - canvas.getBoundingClientRect().top;

//             // Hangi çizgi üzerinde olduğunu bul
//             const lineIndex = parseInt((mouseX - startOffset) / ((lineWidth + lineSpacing)*resulation_rate));

//             // Tüm çizgilerin rengini sıfırla
//             resetLineColors();

//             // Üzerine gelinen çizgiyi rengini değiştirerek tekrar çiz
//             if (lineIndex >= 0 && lineIndex < lineCount) {
//                 changeLineColor(lineIndex);
//             }
//         });

//         // Canvas'ten çıkıldığında
//         canvas.addEventListener('mouseleave', function () {
//             // Tüm çizgilerin rengini sıfırla
//             resetLineColors();
//         });

//         // Çizgi rengini değiştiren fonksiyon
//         function changeLineColor(index) {
//             ctx.strokeStyle = 'white'; // Örnek renk
//             const x = x_coords[index] * resulation_rate
//             ctx.beginPath();
//             ctx.moveTo(x, 0);
//             ctx.lineTo(x, canvas.height);
//             ctx.stroke();
//             console.log(`Çizgi ${index + 1} rengi değiştirildi.`);
//         }

//         // Tüm çizgilerin rengini sıfırlayan fonksiyon
//         function resetLineColors() {
//             ctx.strokeStyle = '#6D95FF'; // Örnek orijinal renk
//             for (let i = 0; i < lineCount; i++) {
//                 const x = (x_coords[i]-min_x) * resulation_rate
//                 ctx.strokeStyle = '#6D95FF'; // Örnek orijinal renk
//                 ctx.beginPath();
//                 ctx.moveTo(x, 0);
//                 ctx.lineTo(x, canvas.height);
//                 ctx.stroke();
//             }
//         }
        
//         function drawSliceLines(cnv_obj, lcs, tcs, slice_dict, responsives){
//             console.log("cnv", cnv_obj, slice_dict);
//             lcs.strokeStyle = '#41d141'; // Örnek orijinal renk
//             let points = slice_dict.points;
//             Object.keys(points).forEach(function(line_name){
//                 let line_direction = points[line_name];
//                 lcs.beginPath();
//                 if (line_name == "vertical"){
//                     lcs.lineWidth = 5;
//                 }else{
//                     lcs.lineWidth = 2;
//                 }
//                 let count = 0;
//                 tcs.font = 'bold 13px Arial';; // Yazı fontunu ve boyutunu ayarla
//                 lcs.fillStyle = '#41d141'; // Yazı rengini ayarla
//                 tcs.fillStyle = '#0022ff'; // Yazı rengini ayarla
//                 Object.keys(line_direction).forEach(function(point_name){
//                     count += 1;
//                     let point_list = line_direction[point_name];
//                     if (count == 1){
//                         lcs.moveTo(point_list[0]/responsives[0], point_list[1]/responsives[1]);
//                         if (line_name == "horizontal" && point_name == "right_point"){
//                             tcs.setTransform(2.5,0,0, 1, -250, 0);
//                             tcs.textBaseline = 'bottom'; // Yazıyı çizgiye yukarıdan başlayarak yerleştir
//                             tcs.fillText(slice_dict.distances.horizontal_points_distance.toFixed(2), point_list[0]/responsives[0], point_list[1]/responsives[1]); // x ve y, yazının başlangıç noktası
//                         }
//                     }else{
//                         if (line_name == "vertical" && point_name == "under_point"){
//                             tcs.setTransform(2.5,0,0, 1, -200, 0);
//                             tcs.textBaseline = 'bottom'; // Yazıyı çizgiye yukarıdan başlayarak yerleştir
//                             tcs.fillText(slice_dict.distances.vertical_points_distance.toFixed(2), point_list[0]/responsives[0], point_list[1]/responsives[1]); // x ve y, yazının başlangıç noktası
//                         }
//                         lcs.lineTo(point_list[0]/responsives[0], point_list[1]/responsives[1]);
//                     }
//                 });
//                 lcs.stroke();
//             });
                
//         }
//         Object.keys(result_dict).forEach(function(key) {
//             const image_w = document.getElementById(`slice_img_${key}`).naturalWidth;
//             const image_h = document.getElementById(`slice_img_${key}`).naturalHeight;
//             const slice_dict = result_dict[key];
//             let img_obj = $(`#slice_img_${key}`)[0];
//             if (img_obj.complete) {
//                 mini_slices_loaded();
//             } else {
//                 // If not loaded, attach a load event handler
//                 img_obj.onload = mini_slices_loaded;
//             }
//             function mini_slices_loaded(){
//                 let cnv_obj = document.getElementById(`lineCanvas_slice_${key}`);
//                 let text_obj = document.getElementById(`lineCanvas_text_${key}`);
//                 let x_res = image_w/cnv_obj.width
//                 let y_res = image_h/cnv_obj.height
//                 let lcs = cnv_obj.getContext('2d');
//                 let tcs = text_obj.getContext('2d');
//                 drawSliceLines(cnv_obj, lcs, tcs, slice_dict, [x_res, y_res])
//             }
//         });
//     };
// });
    





$(document).ready(function(){
    const image = $('#chartImg')[0];
    if (image.complete) {
        imageLoaded();
    } else {
        // If not loaded, attach a load event handler
        image.onload = imageLoaded;
    }

    function imageLoaded() {
        result_dict = dicomResult.result_dict
        result_dict_key = Object.keys(result_dict)
        console.log(result_dict)
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');
        const x_coords = [];
        Object.keys(result_dict).forEach(function(image_x) {
            x_coords.push(image_x);
        });
        const min_x = x_coords[0];
        const max_x = x_coords[x_coords.length - 1];
        
        // 1. Adım: Resmin genişliğini 3'e böl
        const newImageWidth = max_x - min_x;

        // 2. Adım: Canvas genişliğini ve yüksekliğini ayarla
        const image_natural_width = image.naturalWidth;
        const resulation_rate = image.width / image_natural_width;
        canvas.width = (newImageWidth+2)*resulation_rate;
        canvas.height = image.height;
        canvas.style.left = `${(min_x)*resulation_rate}px`
        // 3. Adım: Çizgileri yeni canvas genişliğine göre çiz

        const lineCount = x_coords.length;
        const lineWidth = 0.00001;
        const startOffset = 0;
        const lineSpacing = newImageWidth/lineCount;

        for (let i = 0; i < lineCount; i++) {
            const x = (x_coords[i]-min_x) * resulation_rate
            ctx.strokeStyle = '#6D95FF'; // Örnek orijinal renk
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }

        // Canvas üzerinde tıklama olayını dinle
        canvas.addEventListener('click', function (event) {
            const mouseX = event.clientX - canvas.getBoundingClientRect().left;
            const mouseY = event.clientY - canvas.getBoundingClientRect().top;
        
            // Hangi çizgi üzerinde olduğunu bul
            const lineIndex = parseInt((mouseX - startOffset) / ((lineWidth + lineSpacing)*resulation_rate));
        
            let slice_path = result_dict[result_dict_key[lineIndex]].path
            $('#mini-slice').attr("src", slice_path)
            
            console.log(`Çizgi ${lineIndex + 1} üzerine tıklandı.`);
        });

        // Canvas üzerine gelindiğinde
        // Canvas üzerine gelindiğinde
        canvas.addEventListener('mousemove', function (event) {
            const mouseX = event.clientX - canvas.getBoundingClientRect().left;
            const mouseY = event.clientY - canvas.getBoundingClientRect().top;

            // Hangi çizgi üzerinde olduğunu bul
            const lineIndex = parseInt((mouseX - startOffset) / ((lineWidth + lineSpacing) * resulation_rate));

            // Tüm çizgilerin rengini sıfırla
            resetLineColors();

            // Üzerine gelinen çizgiyi rengini değiştirerek tekrar çiz
            if (lineIndex >= 0 && lineIndex < lineCount) {
                changeLineColor(lineIndex);
            }
        });

        // Çizgi rengini değiştiren fonksiyon
        function changeLineColor(index) {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Canvas'ı temizle
            for (let i = 0; i < lineCount; i++) {
                const x = (x_coords[i] - min_x) * resulation_rate
                ctx.strokeStyle = (i === index) ? 'white' : '#6D95FF'; // Seçilen çizgiyi beyaz, diğerlerini orijinal renk
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }
            console.log(`Çizgi ${index + 1} rengi değiştirildi.`);
        }

        // Tüm çizgilerin rengini sıfırlayan fonksiyon
        function resetLineColors() {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Canvas'ı temizle
            for (let i = 0; i < lineCount; i++) {
                const x = (x_coords[i] - min_x) * resulation_rate
                ctx.strokeStyle = '#6D95FF'; // Örnek orijinal renk
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
                ctx.stroke();
            }
        }
        function drawSliceLines(cnv_obj, lcs, tcs, slice_dict, responsives){
            console.log("cnv", cnv_obj, slice_dict);
            lcs.strokeStyle = '#41d141'; // Örnek orijinal renk
            let points = slice_dict.points;
            Object.keys(points).forEach(function(line_name){
                let line_direction = points[line_name];
                lcs.beginPath();
                if (line_name == "vertical"){
                    lcs.lineWidth = 5;
                }else{
                    lcs.lineWidth = 2;
                }
                let count = 0;
                tcs.font = 'bold 13px Arial';; // Yazı fontunu ve boyutunu ayarla
                lcs.fillStyle = '#41d141'; // Yazı rengini ayarla
                tcs.fillStyle = '#0022ff'; // Yazı rengini ayarla
                Object.keys(line_direction).forEach(function(point_name){
                    count += 1;
                    let point_list = line_direction[point_name];
                    if (count == 1){
                        lcs.moveTo(point_list[0]/responsives[0], point_list[1]/responsives[1]);
                        if (line_name == "horizontal" && point_name == "right_point"){
                            tcs.setTransform(2.5,0,0, 1, -250, 0);
                            tcs.textBaseline = 'bottom'; // Yazıyı çizgiye yukarıdan başlayarak yerleştir
                            tcs.fillText(slice_dict.distances.horizontal_points_distance.toFixed(2), point_list[0]/responsives[0], point_list[1]/responsives[1]); // x ve y, yazının başlangıç noktası
                        }
                    }else{
                        if (line_name == "vertical" && point_name == "under_point"){
                            tcs.setTransform(2.5,0,0, 1, -200, 0);
                            tcs.textBaseline = 'bottom'; // Yazıyı çizgiye yukarıdan başlayarak yerleştir
                            tcs.fillText(slice_dict.distances.vertical_points_distance.toFixed(2), point_list[0]/responsives[0], point_list[1]/responsives[1]); // x ve y, yazının başlangıç noktası
                        }
                        lcs.lineTo(point_list[0]/responsives[0], point_list[1]/responsives[1]);
                    }
                });
                lcs.stroke();
            });
                
        }

        Object.keys(result_dict).forEach(function(key) {
            const image_w = document.getElementById(`slice_img_${key}`).naturalWidth;
            const image_h = document.getElementById(`slice_img_${key}`).naturalHeight;
            const slice_dict = result_dict[key];
            let img_obj = $(`#slice_img_${key}`)[0];
            if (img_obj.complete) {
                mini_slices_loaded();
            } else {
                // If not loaded, attach a load event handler
                img_obj.onload = mini_slices_loaded;
            }
            function mini_slices_loaded(){
                let cnv_obj = document.getElementById(`lineCanvas_slice_${key}`);
                let text_obj = document.getElementById(`lineCanvas_text_${key}`);
                let x_res = image_w/cnv_obj.width
                let y_res = image_h/cnv_obj.height
                let lcs = cnv_obj.getContext('2d');
                let tcs = text_obj.getContext('2d');
                drawSliceLines(cnv_obj, lcs, tcs, slice_dict, [x_res, y_res])
            }
        });
    };
});