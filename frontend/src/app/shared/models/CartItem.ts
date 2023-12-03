import { Film } from "./Film";

export class CartItem {
    //il modificatore inizializza la proprietà film della classe
    constructor(public film:Film)  { }

    price: number = this.film.price;
}