import { Component } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router'

@Component({
  selector: 'pistol',
  templateUrl: './pistol.component.html',
  styleUrls: ['./pistol.component.css']
})

export class PistolComponent  {
  pistol_list: any = [];
  page: number = 1;
  // sortOrder: number = 1;
  filters = { name: '',

};

  constructor(public webService: WebService, private route: ActivatedRoute) {}

  ngOnInit() {
    if (sessionStorage['page']) {
      this.page = Number(sessionStorage['page']);
      }
    this.updateList()

    }

    previousPage() {
      if (this.page > 1) {
        this.page = this.page - 1;
        sessionStorage['page'] = this.page;
        this.updateList()
        }
    }

    nextPage() {
      this.page = this.page + 1;
      sessionStorage['page'] = this.page;
      this.updateList()
    }
    // new stuff for filtering
    updateList(){
      this.pistol_list = this.webService.getPistolSkins(this.page);
    }

    // toggleSort(){
    //   if(this.sortOrder === 1){
    //     this.sortOrder = -1
    //   } else {
    //     this.sortOrder = 1
    //   }
    //   this.updateList();
    // }



  }


