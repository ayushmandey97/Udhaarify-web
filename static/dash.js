$(document).ready(function(){$(document).on('click', '[data-toggle="lightbox"]', function(event) {
                event.preventDefault();
                $(this).ekkoLightbox(
                    {
                        alwaysShowClose: true,
                        onShown: function() {
                            console.log("waiting");
                        }
                        
                    });
            });
                window.onload = function() {
                        $(".rfirst").addClass("rightnow");
                        $(".rsecond").removeClass("rightnow");
                        $(".rthird").removeClass("rightnow");
}


                $("#r1").click(function(){
                        $(".rfirst").addClass("rightnow");
                        $(".rsecond").removeClass("rightnow");
                        $(".rthird").removeClass("rightnow");
                });
                $("#r2").click(function(){
                        $(".rsecond").addClass("rightnow");
                        $(".rfirst").removeClass("rightnow");
                        $(".rthird").removeClass("rightnow");
                });
                $("#r3").click(function(){
                        $(".rthird").addClass("rightnow");
                        $(".rfirst").removeClass("rightnow");
                        $(".rsecond").removeClass("rightnow");
                });

                $('#add-friend').colorbox(); 


    });
  function iframeLoaded() {
      var iFrameID = document.getElementById('idIframe');
      if(iFrameID) {
            // here you can make the height, I delete it first, then I make it again
            iFrameID.height = "";
            iFrameID.height = iFrameID.contentWindow.document.body.scrollHeight + "px";
      }   
  }
parent.iframeLoaded();





