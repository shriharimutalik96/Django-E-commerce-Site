var updateButtons = document.getElementsByClassName("update-cart") //array or list

console.log("Got the request to process");

for(var i=0;i<updateButtons.length;i++){

    // console.log(updateButtons[i])
// Get product ID and action from the updateButtons
    updateButtons[i].addEventListener('click',function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('product_ID : ',productId,'action :',action);

        console.log('USER:',user)

        if(user == 'AnonymousUser'){

            addCookieItem(productId,action);
            //console.log('Not Logged in') // we are not sending the response to the backend if the
                                        // user is not logged in , need to be taken care
        }
        else{
            updateUserOrder(productId,action);
        }

    })



//run this function if the user is guest user
    function addCookieItem(productId,action){

        console.log('User not logged in but...,sending data')

        if(action == 'add'){

            if(cart[productId] == undefined){
                cart[productId] = {'quantity':1}
            }
            else{
                cart[productId]['quantity'] += 1
            }
        }

        if(action == 'remove'){

                cart[productId]['quantity'] -= 1

            if(cart[productId]['quantity']<=0){

                console.log("Remove the item from the cart")

                delete cart[productId]  //delete the productId from the cart object or just delete the key from the cart object
            }

        }

        // printing the cart object
        console.log('Cart'+cart)
        document.cookie = 'cart =' + JSON.stringify(cart) + ";domain=;path='/"
        location.reload()


    }








// Run this function if the user is signed in user
    function updateUserOrder(productId,action){
        console.log('Logged in ,Sending Data ')

        var url ='/update_item/'



        fetch(url,
        {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body : JSON.stringify({'productId':productId,'action':action})
        })




        .then((response)=>{
            return response.json()
        })




        .then((data)=>{
            console.log('data',data)
            location.reload()
        })
    }




}
