import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'skins',
  templateUrl: './skins.component.html',
  styleUrls: ['./skins.component.css']
})

export class SkinsComponent  {
  skins_list: any = [];
  page: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.skins_list = this.webService.getAllSkins(this.page);
    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.skins_list = this.webService.getAllSkins(this.page);
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.skins_list = this.webService.getAllSkins(this.page);
    }

  }


