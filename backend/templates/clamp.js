   const feature_title = document.getElementsByTagName("h1")[0],
            blog_title = document.getElementsByClassName("card-title"),
            post_link = document.getElementsByClassName("post-link"),
            paragraph = document.getElementsByTagName('p');

        function truncate(str,limit){
            if (str.length >= limit){
                return str.slice(0,limit)+'...'
            }
            return  str
        }

        truncate(feature_title,20);
        truncate(blog_title,50);
        truncate(post_link,10);
        truncate(paragraph,1000);
