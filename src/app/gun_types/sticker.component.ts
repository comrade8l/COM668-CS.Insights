import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router'

@Component({
  selector: 'stickers',
  templateUrl: './sticker.component.html',
  styleUrls: ['./sticker.component.css']
})

export class StickerComponent  {
  sticker_list: any = [];
  page: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.sticker_list = this.webService.getStickerSkins(this.page);
    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.sticker_list = this.webService.getStickerSkins(this.page);
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.sticker_list = this.webService.getStickerSkins(this.page);
    }

  }


