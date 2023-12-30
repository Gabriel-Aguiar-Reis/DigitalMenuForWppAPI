import { Component } from '@angular/core';
import { MenuTypeComponent } from '../../components/menu-type/menu-type.component';
import { ShoppingCartComponent } from '../../components/shopping-cart/shopping-cart.component';
import { TypeCardComponent } from '../../components/type-card/type-card.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [MenuTypeComponent, ShoppingCartComponent, TypeCardComponent],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

}
