import { Component } from '@angular/core';
import { ProductCardComponent } from "../product-card/product-card.component";

@Component({
    selector: 'app-type-card',
    standalone: true,
    templateUrl: './type-card.component.html',
    styleUrl: './type-card.component.css',
    imports: [ProductCardComponent]
})
export class TypeCardComponent {

}
