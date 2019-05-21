$( document ).ready(function() {
    let lista=$("#taglist");
    // lista.css("disabled","disabled");
    let tagArray=[]
    $("#list button").click(function(event){
        event.preventDefault();
        value=this.innerHTML;
        let found=tagArray.findIndex(function(e){return e==value});
        console.log(found);
        $(this).toggleClass("clicked");
        if(found==-1)
            tagArray.push(this.innerHTML);
        else
            tagArray.splice(found,1);
        lista.val(tagArray.join(" "));
    });
});