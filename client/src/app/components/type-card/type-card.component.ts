import { Component, OnInit } from '@angular/core';
import { ProductCardComponent } from "../product-card/product-card.component";
import { TypeService } from '../../services/type.service';

@Component({
    selector: 'app-type-card',
    standalone: true,
    templateUrl: './type-card.component.html',
    styleUrl: './type-card.component.css',
    imports: [ProductCardComponent],
    providers: [TypeService]
})
export class TypeCardComponent implements OnInit{
    typeId: string = 'a36de624-acb7-483b-9cc6-7930d51c7473'
    typeName: string = ''

    constructor (private typeService: TypeService) {
    }

    ngOnInit(): void {
        this.typeService.getType(this.typeId).subscribe(
            (response) => {
                this.typeName = response.name
            }
        )
    }

}
