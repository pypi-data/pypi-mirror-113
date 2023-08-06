import{_ as o,w as i,r as t,n as s,h as e,T as n}from"./c.1ff2516f.js";import"./c.f68536d7.js";import{o as a,b as l}from"./index-c0621516.js";let d=class extends e{render(){const o=void 0===this._valid?"":this._valid?"✅":"❌";return n`
      <esphome-process-dialog
        .heading=${`Validate ${this.configuration} ${o}`}
        .type=${"validate"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_openInstall(){l(this.configuration)}_handleProcessDone(o){this._valid=0==o.detail}_handleClose(){this.parentNode.removeChild(this)}};o([i()],d.prototype,"configuration",void 0),o([t()],d.prototype,"_valid",void 0),d=o([s("esphome-validate-dialog")],d);
