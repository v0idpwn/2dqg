    var counter = 1;
    var limit = 20;

    function addInput(divName){
         if (counter == limit){
              alert("You have reached the limit of adding " + counter + " inputs");
         }

         else {
              var div = document.getElementById("Question");
              var form = document.getElementById("container");
              var newdiv = document.createElement("div");
			  clone = div.cloneNode(true);
              clone.id = counter;
              form.insertAdjacentHTML("beforeend", "<h2 class='qTitle'>Question " + (counter+1) + ": </h2>" );
              form.appendChild(clone);
              counter++;
         }

    }
