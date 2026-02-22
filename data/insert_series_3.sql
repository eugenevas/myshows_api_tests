INSERT INTO public.series (name,photo,rating,status,review) VALUES
('Наруто','https://media.myshows.me/shows/760/3/e8/3e8e697187b0fdb49941ecf22db5b9b3.jpg',9,'watching'::public.seriesstatus,'Отличный сериал'),
('Мандалорец','https://media.myshows.me/shows/760/6/61/66124cb92abfa1ae993d66f2e80463fc.jpg',9,'watched'::public.seriesstatus,'Эпично'),
<<<<<<<< HEAD:data/insert_series_3.sql
('Союз спасения. Время гнева','https://media.myshows.me/shows/760/c/64/c6463ee65ae3aeaf071af0f502befc04.jpg',8,'will_watch'::public.seriesstatus,'Интересный сюжет')
========
('Союз спасения. Время гнева','https://media.myshows.me/shows/760/c/64/c6463ee65ae3aeaf071af0f502befc04.jpg',8,'will_watch'::public.seriesstatus,'Интересный сюжет')
RETURNING id
>>>>>>>> c5e8b0d54c770ab92af11b7605668143de6e75a9:data/insert_series.sql
