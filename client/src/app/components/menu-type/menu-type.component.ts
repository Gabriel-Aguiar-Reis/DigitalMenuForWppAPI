import { Component, ElementRef, ViewChild } from '@angular/core';
import { MenuTypeService } from '../../services/menu-type.service';
import { CommonModule } from '@angular/common';

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
    selectedType: string = '';
  
    @ViewChild('menu') menu: ElementRef | undefined;
  
    constructor(private menuTypeService: MenuTypeService) {}
  
    ngOnInit(): void {
      this.menuTypeService.getTypes().subscribe(
        (response: any) => {
          for (const type in response) {
            if (response.hasOwnProperty(type)) {
              // Adiciona apenas o nome do type ao array
              this.types.push(response[type].name);
            }
          }
        }
      );
    }
  
    selectType(type: string) {
      this.selectedType = type;
    }
  
    scrollToType(type: string) {
      if (this.menu) {
        const typeIndex = this.types.findIndex((t) => t === type);
        if (typeIndex !== -1) {
          const typeElement = this.menu.nativeElement.children[typeIndex];
          typeElement.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
        }
      }
    }
  }