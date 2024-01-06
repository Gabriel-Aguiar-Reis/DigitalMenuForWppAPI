import { Component } from '@angular/core';
import { MenuTypeService } from '../../services/menu-type.service';
import { CommonModule } from '@angular/common';
import { ScrollService } from '../../services/scroll.service';

@Component({
    selector: 'app-menu-type',
    standalone: true,
    templateUrl: './menu-type.component.html',
    styleUrl: './menu-type.component.css',
    imports: [CommonModule],
    providers: [MenuTypeService],
})
export class MenuTypeComponent {
    types: string[] = [];
  
    constructor(private menuTypeService: MenuTypeService, private scrollService: ScrollService) {}
  
    ngOnInit(): void {
      this.menuTypeService.getTypes().subscribe(
        (response: any) => {
          for (const type in response) {
            if (response.hasOwnProperty(type)) {
              this.types.push(response[type].name);
            }
          }
        }
      )
    }
    onTypeClick(type: string): void {
      console.log(type)
      this.scrollService.scrollToType.emit(type);
    }
  }