import { Component, OnInit } from '@angular/core';

declare var Twitch: any;

@Component({
    selector: 'app-content',
    templateUrl: './content.component.html',
    styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit {
    constructor() { }

    ngOnInit(): void {
        new Twitch.Embed("twitch-embed", {
            width: "100%",
            height: "480",
            channel: "f0rest",
            layout: "video",
            autoplay: false,
        });
    }
}