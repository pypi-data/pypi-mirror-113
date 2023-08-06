(self["webpackChunknbslide"] = self["webpackChunknbslide"] || []).push([["lib_index_js"],{

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Commands": () => (/* binding */ Commands)
/* harmony export */ });
/* harmony import */ var _iconimport__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./iconimport */ "./lib/iconimport.js");

class Commands {
    constructor(app, pallete, tracker) {
        this.isActive = () => {
            let slideControl = this.activeSlideControl();
            if (slideControl != null) {
                return slideControl.active;
            }
            return false;
        };
        this.activeSlideControl = () => {
            let notebook = this.tracker.currentWidget;
            let result = null;
            this.nbslides.forEach((control, index) => {
                if (control.notebook == notebook) {
                    result = control;
                }
            });
            return result;
        };
        this.nbslides = [];
        this.tracker = tracker;
        this.commands = app.commands;
        this.commands.addCommand('nbslide:start-current', {
            label: "Start presentation in the current Slide",
            icon: _iconimport__WEBPACK_IMPORTED_MODULE_0__.nbslideCurrentIcon,
            isEnabled: () => true,
            isVisible: () => true,
            execute: () => {
                var _a, _b, _c;
                if ((_a = this.activeSlideControl()) === null || _a === void 0 ? void 0 : _a.active) {
                    (_b = this.activeSlideControl()) === null || _b === void 0 ? void 0 : _b.stopPresentation();
                }
                else {
                    (_c = this.activeSlideControl()) === null || _c === void 0 ? void 0 : _c.startPresentation();
                }
            }
        });
        pallete.addItem({
            command: 'nbslide:start-current',
            category: 'nbslide-shortcut'
        });
        this.commands.addCommand('nbslide:start-begin', {
            label: "Start presentation from the first slide",
            icon: _iconimport__WEBPACK_IMPORTED_MODULE_0__.nbslideStartIcon,
            isEnabled: () => true,
            isVisible: () => true,
            execute: () => {
                var _a, _b, _c;
                if ((_a = this.activeSlideControl()) === null || _a === void 0 ? void 0 : _a.active) {
                    (_b = this.activeSlideControl()) === null || _b === void 0 ? void 0 : _b.stopPresentation();
                }
                else {
                    (_c = this.activeSlideControl()) === null || _c === void 0 ? void 0 : _c.startFirst();
                }
            }
        });
        pallete.addItem({
            command: 'nbslide:start-begin',
            category: 'nbslide-shortcut'
        });
        this.commands.addCommand('nbslide:show-all', {
            label: "Stop presentation",
            isEnabled: () => this.isActive(),
            isVisible: () => this.isActive(),
            execute: () => {
                var _a;
                (_a = this.activeSlideControl()) === null || _a === void 0 ? void 0 : _a.stopPresentation();
            }
        });
        pallete.addItem({
            command: 'nbslide:show-all',
            category: 'nbslide-shortcut'
        });
        this.commands.addCommand('nbslide:show-selected', {
            label: "Show current slide",
            isEnabled: () => this.isActive(),
            isVisible: () => this.isActive(),
            execute: () => {
                var _a;
                (_a = this.activeSlideControl()) === null || _a === void 0 ? void 0 : _a.viewCurrentSlide();
            }
        });
        pallete.addItem({
            command: 'nbslide:show-selected',
            category: 'nbslide-shortcut'
        });
        this.commands.addCommand('nbslide:previous-slide', {
            label: "Hide current slide and go to previous one",
            isEnabled: () => this.isActive(),
            isVisible: () => this.isActive(),
            execute: () => {
                var _a;
                (_a = this.activeSlideControl()) === null || _a === void 0 ? void 0 : _a.previousSlide();
            }
        });
        pallete.addItem({
            command: 'nbslide:previous-slide',
            category: 'nbslide-shortcut'
        });
        this.commands.addCommand('nbslide:next-slide', {
            label: "Go to next slide",
            isEnabled: () => this.isActive(),
            isVisible: () => this.isActive(),
            execute: () => {
                var _a;
                (_a = this.activeSlideControl()) === null || _a === void 0 ? void 0 : _a.nextSlide();
            }
        });
        pallete.addItem({
            command: 'nbslide:next-slide',
            category: 'nbslide-shortcut'
        });
    }
    register(nbslide) {
        this.nbslides.push(nbslide);
    }
    unregister(nbslide) {
        this.nbslides = this.nbslides.filter((value, index, arr) => value != nbslide);
    }
}


/***/ }),

/***/ "./lib/iconimport.js":
/*!***************************!*\
  !*** ./lib/iconimport.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "nbslideStartIcon": () => (/* binding */ nbslideStartIcon),
/* harmony export */   "nbslideCurrentIcon": () => (/* binding */ nbslideCurrentIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_img_start_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/img/start.svg */ "./style/img/start.svg");
/* harmony import */ var _style_img_current_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/img/current.svg */ "./style/img/current.svg");



const nbslideStartIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'nbslide:starticon',
    svgstr: _style_img_start_svg__WEBPACK_IMPORTED_MODULE_1__.default,
});
const nbslideCurrentIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'nbslide:currenticon',
    svgstr: _style_img_current_svg__WEBPACK_IMPORTED_MODULE_2__.default,
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _nbslide__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./nbslide */ "./lib/nbslide.js");




/**
 * Initialization data for the nbslide extension.
 */
const plugin = {
    id: 'nbslide:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: (app, pallete, tracker) => {
        console.log('JupyterLab extension nbslide is activated!');
        let commands = new _commands__WEBPACK_IMPORTED_MODULE_2__.Commands(app, pallete, tracker);
        app.docRegistry.addWidgetExtension('Notebook', new _nbslide__WEBPACK_IMPORTED_MODULE_3__.NbSlide(commands));
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/nbslide.js":
/*!************************!*\
  !*** ./lib/nbslide.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NbSlide": () => (/* binding */ NbSlide)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _slidecontrol__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./slidecontrol */ "./lib/slidecontrol.js");


class NbSlide {
    constructor(commands) {
        this.commands = commands;
    }
    createNew(widget, context) {
        //eval("window.widget = widget;");
        //eval("window.context = context;");
        let slideControl = new _slidecontrol__WEBPACK_IMPORTED_MODULE_1__.SlideControl(widget, this.commands);
        this.commands.register(slideControl);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => {
            slideControl.dispose();
            this.commands.unregister(slideControl);
        });
    }
}


/***/ }),

/***/ "./lib/slidecontrol.js":
/*!*****************************!*\
  !*** ./lib/slidecontrol.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SlideControl": () => (/* binding */ SlideControl)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_2__);



function isSlideCell(cell) {
    let slideshow = cell.model.metadata.get('slideshow');
    let slidetype = slideshow ? slideshow.slide_type : null;
    return ((slidetype == "slide") || (slidetype == "subslide") || (slidetype == "fragment"));
}
function isSubSlide(cell) {
    let slideshow = cell.model.metadata.get('slideshow');
    let slidetype = slideshow ? slideshow.slide_type : null;
    return ((slidetype == "subslide"));
}
function isMainSlide(cell) {
    let slideshow = cell.model.metadata.get('slideshow');
    let slidetype = slideshow ? slideshow.slide_type : null;
    return ((slidetype == "slide"));
}
function isInvisibleCell(cell) {
    let slideshow = cell.model.metadata.get('slideshow');
    let slidetype = slideshow ? slideshow.slide_type : null;
    return ((slidetype == "skip") || (slidetype == "notes"));
}
function isNoScroll(cell) {
    let tags = cell.model.metadata.get('tags') || [];
    return tags.includes('noscroll');
}
function skipExecution(cell) {
    let tags = cell.model.metadata.get('tags') || [];
    return (cell.model.type != "code") || tags.includes('skiprun');
}
class SlideControl {
    constructor(notebook, commands) {
        this.findSlideNumber = (index) => {
            let total = 0;
            let cells = this.notebook.content.widgets;
            let result = 0;
            cells.forEach((cell, currentindex) => {
                if (isSlideCell(cell)) {
                    total += 1;
                }
                if (currentindex == index) {
                    result = total;
                }
            });
            this.total = total;
            return result;
        };
        this.getSlideIndex = (index) => {
            let cells = this.notebook.content.widgets;
            for (let i = index; i >= 0; i--) {
                let cell = cells[i];
                if (isSlideCell(cell)) {
                    return i;
                }
            }
            return 0;
        };
        this.viewSlide = (firstIndex) => {
            let cells = this.notebook.content.widgets;
            let index = firstIndex;
            if (isSubSlide(cells[index])) {
                let subindex = index;
                do {
                    subindex = this.getSlideIndex(subindex - 1);
                    this.hideSlide(subindex);
                } while ((subindex != 0) && !isMainSlide(cells[subindex]));
            }
            let noScroll = false;
            do {
                let cell = cells[index];
                noScroll = noScroll || isNoScroll(cell);
                if (!isInvisibleCell(cell)) {
                    cell.show();
                }
                this.updateSlideShowConfig(cell);
                if (this.autosuffix && (cell.model.type == "markdown")) {
                    let nodes = cell.node.querySelectorAll('h1, h2, h3, h4, h5, h6');
                    if (nodes.length !== 0) {
                        let el = nodes[0];
                        let suffix = el.textContent;
                        if (suffix !== null) {
                            this.suffix = suffix.replace('¶', '');
                        }
                    }
                }
                this.updateSlideShowConfig(cell);
                if (!noScroll) {
                    _lumino_domutils__WEBPACK_IMPORTED_MODULE_2__.ElementExt.scrollIntoViewIfNeeded(this.notebook.content.node, cell.node);
                }
                index++;
            } while ((index < cells.length) && !isSlideCell(cells[index]));
            if (!noScroll) {
                _lumino_domutils__WEBPACK_IMPORTED_MODULE_2__.ElementExt.scrollIntoViewIfNeeded(this.notebook.content.node, cells[firstIndex].node);
            }
            this.updateSlideTitle();
            return index;
        };
        this.monitorProgression = (sender, cell) => {
            if (this.active) {
                this.currentSlide = this.findSlideNumber(sender.activeCellIndex);
                this.updateSlideNumber();
            }
        };
        this.startFirst = () => {
            let first = -1;
            let cells = this.notebook.content.widgets;
            cells.forEach((cell, index) => {
                if (isSlideCell(cell) && (first == -1)) {
                    first = index;
                }
            });
            if (first == -1) {
                first = 0;
            }
            this.notebook.content.activeCellIndex = first;
            this.startPresentation();
        };
        this.startPresentation = () => {
            this.notebook.toolbar.layout.widgets.forEach((toolbaritem, index) => {
                if (!toolbaritem.hasClass('jp-Toolbar-spacer')) {
                    toolbaritem.hide();
                }
            });
            this.slidePosition.show();
            this.slideTitle.show();
            this.active = true;
            this.notebook.content.activeCellChanged.connect(this.monitorProgression);
            let currentSlide = this.getSlideIndex(this.notebook.content.activeCellIndex);
            console.log(currentSlide);
            let cells = this.notebook.content.widgets;
            for (let index = 0; index < cells.length;) {
                if (index <= currentSlide) {
                    index = this.viewSlide(index);
                }
                else {
                    cells[index].hide();
                    index++;
                }
            }
            this.notebook.content.scrollToCell(cells[currentSlide]);
            this.notebook.content.activeCellIndex = currentSlide;
            this.currentSlide = this.findSlideNumber(currentSlide);
            this.updateSlideNumber();
            this.updateSlideTitle();
            document.documentElement.requestFullscreen();
            this.notebook.content.deselectAll();
            //alert('ok ' + this.title);
        };
        this.stopPresentation = () => {
            this.notebook.toolbar.layout.widgets.forEach((toolbaritem, index) => {
                toolbaritem.show();
            });
            this.slidePosition.hide();
            this.slideTitle.hide();
            let cells = this.notebook.content.widgets;
            cells.forEach((cell, index) => {
                cell.show();
            });
            this.active = false;
            this.notebook.content.activeCellChanged.disconnect(this.monitorProgression);
            if (document.fullscreenElement !== null) {
                document.exitFullscreen();
            }
        };
        this.viewCurrentSlide = () => {
            this.viewSlide(this.notebook.content.activeCellIndex);
        };
        this.hideSlide = (firstIndex) => {
            let cells = this.notebook.content.widgets;
            cells[firstIndex].hide();
            for (let index = firstIndex + 1; index < cells.length; index++) {
                if (isSlideCell(cells[index])) {
                    break;
                }
                cells[index].hide();
            }
        };
        this.previousSlide = () => {
            let cells = this.notebook.content.widgets;
            let firstIndex = this.getSlideIndex(this.notebook.content.activeCellIndex);
            if (firstIndex == 0) {
                _lumino_domutils__WEBPACK_IMPORTED_MODULE_2__.ElementExt.scrollIntoViewIfNeeded(this.notebook.content.node, cells[firstIndex].node);
                return;
            }
            this.hideSlide(firstIndex);
            let previousIndex = this.getSlideIndex(firstIndex - 1);
            this.viewSlide(previousIndex);
            _lumino_domutils__WEBPACK_IMPORTED_MODULE_2__.ElementExt.scrollIntoViewIfNeeded(this.notebook.content.node, cells[previousIndex].node);
            this.notebook.content.activeCellIndex = previousIndex;
            this.viewCurrentSlide();
        };
        this.nextSlide = () => {
            let cells = this.notebook.content.widgets;
            let index = this.notebook.content.activeCellIndex;
            if (cells[index].isHidden) {
                index = this.getSlideIndex(index);
            }
            else {
                for (index = index + 1; index < cells.length; index++) {
                    if (isSlideCell(cells[index])) {
                        break;
                    }
                }
                if (index == cells.length) {
                    index -= 1;
                }
            }
            let shouldRun = cells[index].isHidden;
            let start = index;
            this.viewSlide(index);
            do {
                if (shouldRun && !skipExecution(cells[index])) {
                    this.notebook.content.activeCellIndex = index;
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookActions.run(this.notebook.content, this.notebook.sessionContext);
                }
                index++;
            } while ((index < cells.length) && !isSlideCell(cells[index]));
            this.notebook.content.activeCellIndex = start;
        };
        this.currentSlide = 0;
        this.total = 0;
        this.notebook = notebook;
        this.active = false;
        this.title = notebook.title.label;
        this.suffix = "";
        this.autosuffix = true;
        this.slidePosition = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            className: 'positionSlideshow',
            onClick: this.stopPresentation,
            tooltip: 'Stop presentation',
            label: '1',
        });
        this.slidePosition.hide();
        this.slideTitle = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            className: 'titleSlideshow',
            onClick: this.stopPresentation,
            tooltip: 'Stop presentation',
            label: notebook.title.label,
        });
        this.slideTitle.hide();
        this.startButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.CommandToolbarButton({
            commands: commands.commands,
            id: 'nbslide:start-begin'
        });
        this.startButton.addClass('jp-nbslide-nbtoolbarbutton');
        this.startCurrentButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.CommandToolbarButton({
            commands: commands.commands,
            id: 'nbslide:start-current'
        });
        this.startCurrentButton.addClass('jp-nbslide-nbtoolbarbutton');
        notebook.toolbar.insertItem(0, 'nbslide-current', this.startCurrentButton);
        notebook.toolbar.insertItem(0, 'nbslide-slideshow', this.startButton);
        notebook.toolbar.insertItem(0, 'nbslide-position', this.slidePosition);
        notebook.toolbar.insertItem(notebook.toolbar.layout.widgets.length - 1, 'nbslide-title', this.slideTitle);
    }
    updateSlideShowConfig(cell) {
        let slideshow = cell.model.metadata.get('slideshow');
        if (slideshow == null) {
            return;
        }
        let configs = slideshow;
        if (configs.hasOwnProperty('slide_title')) {
            this.title = configs.slide_title;
        }
        if (configs.hasOwnProperty('slide_suffix')) {
            this.suffix = configs.slide_suffix;
        }
        if (configs.hasOwnProperty('slide_autosuffix')) {
            this.autosuffix = configs.slide_autosuffix;
        }
    }
    setSlideTitle(title) {
        this.slideTitle.props.label = title;
        this.slideTitle.update();
    }
    updateSlideNumber() {
        this.setSlideNumber(this.currentSlide + '/' + this.total);
    }
    updateSlideTitle() {
        this.setSlideTitle(this.title + (this.suffix ? ` - ${this.suffix}` : ''));
    }
    setSlideNumber(number) {
        this.slidePosition.props.label = number;
        this.slidePosition.update();
    }
    dispose() {
        this.slidePosition.dispose();
        this.slideTitle.dispose();
        this.startButton.dispose();
        this.startCurrentButton.dispose();
    }
}


/***/ }),

/***/ "./style/img/current.svg":
/*!*******************************!*\
  !*** ./style/img/current.svg ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   xmlns:svg=\"http://www.w3.org/2000/svg\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   fill=\"none\"\n   viewBox=\"0 0 14 14\"\n   height=\"14\"\n   width=\"14\"\n   version=\"1.1\">\n  <path\n     fill=\"#616161\"\n     class=\"jp-icon3\"\n     d=\"M 1,2.9 C 1,3.15 1.25,3.4 1.5,3.4 H 2 V 8.1 C 2,8.35 2.25,8.6 2.5,8.6 H 6.45 L 6.4499798,9.6360626 5.15811,10.719141 c -0.191515,0.160701 -0.22233,0.512915 -0.061629,0.704431 0.1607,0.191515 0.5129145,0.222329 0.7044298,0.06163 L 6.95,10.521 8.0990903,11.485201 c 0.1915155,0.160701 0.5437304,0.129886 0.7044305,-0.06163 0.1606994,-0.191516 0.1298847,-0.54373 -0.06163,-0.70443 L 7.4499998,9.6360626 7.45,8.6 h 3.95 c 0.25,0 0.5,-0.25 0.5,-0.5 V 3.4 h 0.5 c 0.25,0 0.5,-0.25 0.5,-0.5 0,-0.25 -0.25,-0.5 -0.5,-0.5 H 1.5 C 1.25,2.4 1,2.65 1,2.9 Z m 2,0.5 h 7.9 V 7.6 H 3 Z\"\n     />\n   <path\n     fill=\"#616161\"\n     class=\"jp-icon3\"\n     d=\"m 3.7,4.4 h 2.7 v 2 H 3.7 z M 4.2,4.9 V 5.9 h 1.7 V 4.9 Z\"\n     />\n  <g\n     transform=\"translate(0,-0.00695096)\">\n    <path\n       fill=\"#616161\"\n       class=\"jp-icon3\"\n       d=\"m 8.0002756,4.1818738 h 2.1835924 c 0.125,0 0.25,0.125 0.25,0.25 0,0.1250005 -0.125,0.2500005 -0.25,0.25 H 8.0002756 c -0.125,5e-7 -0.25,-0.1249995 -0.25,-0.25 0,-0.125 0.125,-0.25 0.25,-0.25 z\"\n       />\n    <path\n       fill=\"#616161\"\n       class=\"jp-icon3\"\n       d=\"m 8.0002756,5.1983585 h 2.1835924 c 0.125,0 0.25,0.125 0.25,0.25 0,0.1250005 -0.125,0.2500005 -0.25,0.25 H 8.0002756 c -0.125,5e-7 -0.25,-0.1249995 -0.25,-0.25 0,-0.125 0.125,-0.25 0.25,-0.25 z\"\n       />\n    <path\n       fill=\"#616161\"\n       class=\"jp-icon3\"\n       d=\"m 8.0002756,6.2148437 h 2.1835924 c 0.125,0 0.25,0.125 0.25,0.25 0,0.1250005 -0.125,0.2500005 -0.25,0.25 H 8.0002756 c -0.125,5e-7 -0.25,-0.1249995 -0.25,-0.25 0,-0.125 0.125,-0.25 0.25,-0.25 z\"\n       />\n  </g>\n</svg>\n");

/***/ }),

/***/ "./style/img/start.svg":
/*!*****************************!*\
  !*** ./style/img/start.svg ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   xmlns:svg=\"http://www.w3.org/2000/svg\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   fill=\"none\"\n   viewBox=\"0 0 14 14\"\n   height=\"14\"\n   width=\"14\"\n   version=\"1.1\">\n  <path\n     fill=\"#616161\"\n     class=\"jp-icon3\"\n     d=\"M 1,2.9 C 1,3.15 1.25,3.4 1.5,3.4 H 2 V 8.1 C 2,8.35 2.25,8.6 2.5,8.6 H 6.45 L 6.4499798,9.6360626 5.15811,10.719141 c -0.191515,0.160701 -0.22233,0.512915 -0.061629,0.704431 0.1607,0.191515 0.5129145,0.222329 0.7044298,0.06163 L 6.95,10.521 8.0990903,11.485201 c 0.1915155,0.160701 0.5437304,0.129886 0.7044305,-0.06163 0.1606994,-0.191516 0.1298847,-0.54373 -0.06163,-0.70443 L 7.4499998,9.6360626 7.45,8.6 h 3.95 c 0.25,0 0.5,-0.25 0.5,-0.5 V 3.4 h 0.5 c 0.25,0 0.5,-0.25 0.5,-0.5 0,-0.25 -0.25,-0.5 -0.5,-0.5 H 1.5 C 1.25,2.4 1,2.65 1,2.9 Z m 2,0.5 h 7.9 V 7.6 H 3 Z\"\n     />\n  <path\n     fill=\"#616161\"\n     class=\"jp-icon3\"\n     d=\"M 5.8336309,4.0361844 V 6.9916698 L 8.4287211,5.4933937 Z\"\n     />\n</svg>\n");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.4e90c9679512f2f64773.js.map