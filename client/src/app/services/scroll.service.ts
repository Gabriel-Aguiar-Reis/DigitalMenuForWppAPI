import { Injectable, EventEmitter } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ScrollService {
  public scrollToType = new EventEmitter<string>()

  constructor() {}
}