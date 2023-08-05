(self["webpackChunkjupyterlab_wipp"] = self["webpackChunkjupyterlab_wipp"] || []).push([["lib_index_js"],{

/***/ "./lib/components/collectionTypeSwitcherWidget.js":
/*!********************************************************!*\
  !*** ./lib/components/collectionTypeSwitcherWidget.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SwitcherWidget": () => (/* binding */ SwitcherWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Switcher widget for choosing WIPP Collection type to explore
 */
class SwitcherWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(switchType) {
        super();
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout());
        const switchPanel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        let ul = document.createElement('ul');
        ul.className = 'wipp-WippSidebar-switcher-list';
        let li1 = document.createElement('li');
        li1.className = 'wipp-WippSidebar-switcher-item';
        this._imageCollectionsButton = document.createElement('button');
        this._imageCollectionsButton.className = 'selected';
        this._imageCollectionsButton.value = 'Image Collections';
        this._imageCollectionsButton.onclick = () => {
            this._imageCollectionsButton.className = 'selected';
            this._csvCollectionsButton.className = 'normal';
            switchType(1);
        };
        this._imageCollectionsButton.innerText = 'Image Collections';
        li1.appendChild(this._imageCollectionsButton);
        ul.appendChild(li1);
        let li2 = document.createElement('li');
        li2.className = 'wipp-WippSidebar-switcher-item';
        this._csvCollectionsButton = document.createElement('button');
        this._csvCollectionsButton.className = 'normal';
        this._csvCollectionsButton.value = 'CSV Collections';
        this._csvCollectionsButton.onclick = () => {
            this._csvCollectionsButton.className = 'selected';
            this._imageCollectionsButton.className = 'normal';
            switchType(2);
        };
        this._csvCollectionsButton.innerText = 'CSV Collections';
        li2.appendChild(this._csvCollectionsButton);
        ul.appendChild(li2);
        switchPanel.node.appendChild(ul);
        layout.addWidget(switchPanel);
    }
}


/***/ }),

/***/ "./lib/components/searchWidget.js":
/*!****************************************!*\
  !*** ./lib/components/searchWidget.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SearchWidget": () => (/* binding */ SearchWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);



/**
 * Search widget on top of WIPP Panel.
 */
class SearchWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(placeholder, updateWidget) {
        super();
        this._getPlaceholder = placeholder;
        this.addClass('wipp-WippSidebar-search-layout');
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout());
        // Search input bar for imageCollections
        const searchBar = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        searchBar.addClass('wipp-WippSidebar-search');
        this._searchBar = document.createElement('input');
        this._searchBar.placeholder = this._getPlaceholder();
        this._searchBar.oninput = async () => {
            updateWidget(this._searchBar.value);
        };
        searchBar.node.appendChild(this._searchBar);
        layout.addWidget(searchBar);
        // Clear search bar button
        const clearButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            tooltip: 'CLEAR SEARCH BAR:',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.closeIcon,
            onClick: async () => {
                updateWidget("");
                this._searchBar.value = "";
            }
        });
        layout.addWidget(clearButton);
        // Search button
        const searchButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.searchIcon,
            onClick: async () => {
                updateWidget(this._searchBar.value);
            }
        });
        layout.addWidget(searchButton);
    }
    onUpdateRequest() {
        this._searchBar.value = "";
        this._searchBar.placeholder = this._getPlaceholder();
    }
}


/***/ }),

/***/ "./lib/components/tableWidget.js":
/*!***************************************!*\
  !*** ./lib/components/tableWidget.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableHeaderComponent": () => (/* binding */ TableHeaderComponent),
/* harmony export */   "TableRowComponent": () => (/* binding */ TableRowComponent),
/* harmony export */   "GenericTableWidget": () => (/* binding */ GenericTableWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

/*
* React Component for table header
*/
function TableHeaderComponent(props) {
    const tableHeaders = props.headers.map((value) => {
        return (
        // Column headers are clickable and will sort by that column on click
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("th", { onClick: evt => {
                props.sortFunction(value[0]);
                evt.stopPropagation();
            } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
                " ",
                value[1],
                " "),
            (value[0] == props.tableSortedKey && props.tableSortedDirection == true) && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "wipp-WippSidebar-table-header-sorted-ascending" }, " "),
            (value[0] == props.tableSortedKey && props.tableSortedDirection == false) && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "wipp-WippSidebar-table-header-sorted-descending" }, " ")));
    });
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", null,
        tableHeaders,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("th", { className: "wipp-WippSidebar-table-header-import-column" })));
}
/**
 * React Component for table row containing single imageCollection
 */
function TableRowComponent(props) {
    const { el, headers, collectionUrl, injectCode } = props;
    // function to convert imagecollection size to human-readable format
    const sizeof = (bytes) => {
        if (bytes == 0) {
            return "0.00 B";
        }
        const e = Math.floor(Math.log(bytes) / Math.log(1024));
        return (bytes / Math.pow(1024, e)).toFixed(0) + ' ' + ' KMGTP'.charAt(e) + 'B';
    };
    // Convert creation timestamp to human-readable format
    const date = new Date(el.creationDate.replace(/\b\+0000/g, ''));
    const allElsTemplates = {
        name: react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null,
            " ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { href: collectionUrl + el.id, target: "_blank" },
                " ",
                el.name,
                " "),
            " "),
        numberOfImages: react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", { className: "wipp-WippSidebar-table-element" },
            " ",
            el.numberOfImages,
            " "),
        imagesTotalSize: react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", { className: "wipp-WippSidebar-table-element" },
            " ",
            sizeof(el.imagesTotalSize),
            " "),
        creationDate: react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", { className: "wipp-WippSidebar-table-element" },
            " ",
            date.toLocaleString(),
            " "),
    };
    const els = headers.map((value) => {
        if (value[0] == 'name')
            return allElsTemplates.name;
        if (value[0] == 'numberOfImages')
            return allElsTemplates.numberOfImages;
        if (value[0] == 'imagesTotalSize')
            return allElsTemplates.imagesTotalSize;
        if (value[0] == 'creationDate')
            return allElsTemplates.creationDate;
    });
    // return tr element
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", null,
        els,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", className: "bp3-button bp3-minimal jp-ToolbarButtonComponent minimal jp-Button", onClick: evt => {
                    injectCode(el.id);
                    evt.stopPropagation();
                } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { className: "wipp-ImportIcon jp-Icon jp-Icon-16" })))));
}
// Generic class for different types of tables (ImageCollection, CsvCollection, etc)
class GenericTableWidget extends react__WEBPACK_IMPORTED_MODULE_0__.Component {
    constructor(props) {
        super(props);
        this.state = {
            tableSortedKey: 'creationDate',
            tableSortedDirection: true
        };
    }
    // Apply sort to WIPP Collections Array
    // Update the React State
    sort(key) {
        let ar = this.props.ar;
        let direction = this.state.tableSortedDirection;
        if (key == this.state.tableSortedKey) {
            direction = !direction;
        }
        ar.sort(function (a, b) {
            const x = a[key];
            const y = b[key];
            if (direction === true) {
                return ((x < y) ? -1 : ((x > y) ? 1 : 0));
            }
            else {
                return ((x > y) ? -1 : ((x < y) ? 1 : 0));
            }
        });
        this.setState({ tableSortedDirection: direction, tableSortedKey: key });
    }
    render() {
        // Generate headers and rows of the table
        const tableHeaders = react__WEBPACK_IMPORTED_MODULE_0___default().createElement(TableHeaderComponent, { headers: this.props.tableHeader, tableSortedKey: this.state.tableSortedKey, tableSortedDirection: this.state.tableSortedDirection, sortFunction: key => this.sort(key) });
        const tableRows = this.props.ar.map((e) => react__WEBPACK_IMPORTED_MODULE_0___default().createElement(TableRowComponent, { key: e.id, el: e, headers: this.props.tableHeader, collectionUrl: this.props.collectionUrl, injectCode: this.props.codeInjector }));
        // Assemble headers and rows in the full table
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("table", { className: 'wipp-WippSidebar-table' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("thead", null, tableHeaders),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tbody", null, tableRows))));
    }
}
;


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'wipp', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, 'Not a JSON response body.');
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _notebookInfoBox__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./notebookInfoBox */ "./lib/notebookInfoBox.js");
/* harmony import */ var _wippRegister__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./wippRegister */ "./lib/wippRegister.js");
/* harmony import */ var _sidebar__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./sidebar */ "./lib/sidebar.js");










/**
 * Initialization data for the jupyterlab_wipp extension.
 */
const plugin = {
    id: 'jupyterlab_wipp:plugin',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__.IFileBrowserFactory, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker],
    activate: (app, palette, mainMenu, notebookTracker, factory, labShell, consoleTracker) => {
        // Run initial health check on backend handlers and check WIPP API is available
        (0,_handler__WEBPACK_IMPORTED_MODULE_6__.requestAPI)('info')
            .then(response => {
            console.debug(response.data);
            if (response.code == 200) {
                // Show dialogs and register notebooks
                function registerByPath(path) {
                    // Launch dialog form to collect notebook name and description
                    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: 'Register Notebook in WIPP',
                        body: new _notebookInfoBox__WEBPACK_IMPORTED_MODULE_7__.NotebookInfoForm()
                    }).then(result => {
                        if (!result.button.accept) {
                            console.debug('Notebook registering cancelled by user.');
                            return;
                        }
                        const info = result.value;
                        console.debug(`Form accepted. Name: ${info.name}. Description: ${info.description}`);
                        // Launch WippRegister dialog
                        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: 'Waiting for WIPP...',
                            body: new _wippRegister__WEBPACK_IMPORTED_MODULE_8__.WippRegister(path, info.name, info.description, info.openInWipp),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'DISMISS' })]
                        });
                    });
                }
                // Create command for context menu
                const registerContextMenuCommandID = 'wipp-register-context-menu';
                app.commands.addCommand(registerContextMenuCommandID, {
                    label: 'Register in WIPP',
                    iconClass: 'jp-MaterialIcon jp-LinkIcon',
                    isVisible: () => factory.tracker.currentWidget.selectedItems().next().type === 'notebook',
                    execute: () => registerByPath(factory.tracker.currentWidget.selectedItems().next().path)
                });
                // Add command to context menu
                const selectorItem = '.jp-DirListing-item[data-isdir]';
                app.contextMenu.addItem({
                    command: registerContextMenuCommandID,
                    selector: selectorItem
                });
                //Create command for main menu
                const registerFileMenuCommandID = 'wipp-register-menu';
                app.commands.addCommand(registerFileMenuCommandID, {
                    label: 'Register in WIPP',
                    iconClass: 'jp-MaterialIcon jp-LinkIcon',
                    isVisible: () => notebookTracker.currentWidget !== null && notebookTracker.currentWidget === app.shell.currentWidget,
                    execute: () => registerByPath(notebookTracker.currentWidget.context.path)
                });
                // Add command to the main menu
                mainMenu.fileMenu.addGroup([
                    {
                        command: registerFileMenuCommandID,
                    }
                ], 40 /* rank */);
                // Add command to the palette
                palette.addItem({
                    command: registerFileMenuCommandID,
                    category: 'WIPP',
                    args: {}
                });
                // Create the WIPP sidebar panel
                const sidebar = new _sidebar__WEBPACK_IMPORTED_MODULE_9__.WippSidebar(app, notebookTracker, consoleTracker);
                sidebar.id = 'wipp-labextension:plugin';
                sidebar.title.iconClass = 'wipp-WippLogo jp-SideBar-tabIcon';
                sidebar.title.caption = 'WIPP';
                // Register sidebar panel with JupyterLab
                labShell.add(sidebar, 'left', { rank: 200 });
            }
        })
            .catch(reason => {
            throw new Error(`The jupyterlab_wipp server extension appears to be missing.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/notebookInfoBox.js":
/*!********************************!*\
  !*** ./lib/notebookInfoBox.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NotebookInfoForm": () => (/* binding */ NotebookInfoForm)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The UI for registering notebook in WIPP
 * Form asks user for notebook name and description
 */
class NotebookInfoForm extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        super();
        this.node.appendChild(this.createBody());
    }
    createBody() {
        const node = document.createElement('div');
        const text = document.createElement('span');
        this._name = document.createElement('input');
        this._description = document.createElement('input');
        node.className = 'jp-RedirectForm';
        text.textContent = 'Enter notebook name and description';
        this._name.placeholder = 'Notebook name';
        this._description.placeholder = 'Short description';
        this._openInWipp = document.createElement('input');
        this._openInWipp.type = "checkbox";
        this._openInWipp.id = "open-in-wipp";
        this._openInWipp.checked = true;
        this._openInWipp.style.display = 'inline';
        this._openInWipp.style.width = 'fit-content';
        const label = document.createElement('label');
        label.htmlFor = "open-in-wipp";
        label.appendChild(document.createTextNode('Show in WIPP'));
        node.appendChild(text);
        node.appendChild(this._name);
        node.appendChild(this._description);
        node.appendChild(this._openInWipp);
        node.appendChild(label);
        return node;
    }
    /**
     * Returns the input value.
     */
    getValue() {
        let info = {
            name: this._name.value,
            description: this._description.value,
            openInWipp: this._openInWipp.checked
        };
        return info;
    }
}


/***/ }),

/***/ "./lib/sidebar.js":
/*!************************!*\
  !*** ./lib/sidebar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "WippSidebar": () => (/* binding */ WippSidebar),
/* harmony export */   "insertInputPath": () => (/* binding */ insertInputPath),
/* harmony export */   "getCurrentEditor": () => (/* binding */ getCurrentEditor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _components_tableWidget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/tableWidget */ "./lib/components/tableWidget.js");
/* harmony import */ var _components_searchWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/searchWidget */ "./lib/components/searchWidget.js");
/* harmony import */ var _components_collectionTypeSwitcherWidget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/collectionTypeSwitcherWidget */ "./lib/components/collectionTypeSwitcherWidget.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);









/**
 * Sidebar widget for displaying WIPP image collections.
 */
class WippSidebar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Create a new WIPP sidebar.
     */
    constructor(app, notebookTracker, consoleTracker) {
        super();
        this._collection_url_prefix = '';
        this._objectArray = [];
        this._tableHeader = [];
        this._search_placeholder = '';
        this.handleClick = () => { };
        this._valueChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this.app = app;
        this.notebookTracker = notebookTracker;
        this.consoleTracker = consoleTracker;
        this._tableState = {
            collections_array: this._objectArray,
            code_injector: this.handleClick,
            tableHeader: this._tableHeader,
            collection_url_prefix: this._collection_url_prefix
        };
        this.addClass('wipp-WippSidebar');
        // Call API to get UI URLs
        this._getUiUrls();
        // Define Widget layout
        let layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.PanelLayout());
        // Add search bar widget for search WIPP Collections
        this._search = new _components_searchWidget__WEBPACK_IMPORTED_MODULE_5__.SearchWidget(() => this.get_search_placeholder(), (arg0) => this._searchCollections(arg0));
        layout.addWidget(this._search);
        // Add buttons to choose type of WIPP Collection
        this._switcher = new _components_collectionTypeSwitcherWidget__WEBPACK_IMPORTED_MODULE_6__.SwitcherWidget((arg0) => this.swithchCollectionType(arg0));
        layout.addWidget(this._switcher);
        // Add ReactWidget for table of WIPP Collections
        this._table = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.UseSignal, { signal: this._valueChanged, initialArgs: this._tableState }, (_, oa) => react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_components_tableWidget__WEBPACK_IMPORTED_MODULE_7__.GenericTableWidget, { ar: oa.collections_array, codeInjector: oa.code_injector, tableHeader: oa.tableHeader, collectionUrl: oa.collection_url_prefix })));
        this._table.addClass('wipp-WippSidebar-table-div');
        layout.addWidget(this._table);
        this.swithchCollectionType(1);
    }
    swithchCollectionType(choice) {
        let app = this.app;
        let notebookTracker = this.notebookTracker;
        let consoleTracker = this.consoleTracker;
        let file_path_prefix;
        let file_path_suffix;
        switch (choice) {
            case 1: { // Show Image Collections
                this._search_collection_type_url = 'imageCollections/search';
                this._get_collection_type_url = 'imageCollections';
                file_path_prefix = "'/opt/shared/wipp/collections/";
                file_path_suffix = "/images/'";
                // specify table header
                this._tableHeader = [['name', 'Name'], ['numberOfImages', '# of images'], ['imagesTotalSize', 'Total size'], ['creationDate', 'Creation date']];
                // set search bar placeholder
                this._search_placeholder = 'SEARCH IMAGE COLLECTIONS';
                // set collection UI url prefix
                this._collection_url_prefix = this._imagescollection_url;
                break;
            }
            case 2: { // Show CSV Collections
                this._search_collection_type_url = 'csvCollections/search';
                this._get_collection_type_url = 'csvCollections';
                file_path_prefix = "'/opt/shared/wipp/csv-collections/";
                file_path_suffix = "'";
                // specify table header
                this._tableHeader = [['name', 'Name'], ['creationDate', 'Creation date']];
                // set search bar placeholder
                this._search_placeholder = 'SEARCH CSV COLLECTIONS';
                // set collection UI url prefix
                this._collection_url_prefix = this._csvcollections_url;
                break;
            }
        }
        // define function for pasting code to current editor
        this.handleClick = function handleClick(id) {
            const editor = getCurrentEditor(app, notebookTracker, consoleTracker);
            if (editor) {
                insertInputPath(editor, file_path_prefix + id + file_path_suffix);
            }
            ;
        };
        // Update search bar
        this._search.update();
        // Update Table with the new type immediately
        this._tableState.tableHeader = this._tableHeader;
        this._tableState.code_injector = this.handleClick;
        this._tableState.collection_url_prefix = this._collection_url_prefix;
        this._getAllCollections();
    }
    async _getUiUrls() {
        // Return results of API request
        (0,_handler__WEBPACK_IMPORTED_MODULE_8__.requestAPI)('ui_urls', {})
            .then(response => {
            this._imagescollection_url = response.imagescollection;
            this._csvcollections_url = response.csvcollections;
        });
    }
    async _getAllCollections() {
        // Display results of API request
        (0,_handler__WEBPACK_IMPORTED_MODULE_8__.requestAPI)(this._get_collection_type_url, {})
            .then((objectArray) => {
            // Update internal variable
            this._objectArray = objectArray;
            this._tableState.collections_array = objectArray;
            // Send signal for table widget to update data
            this._valueChanged.emit(this._tableState);
        });
    }
    async _searchCollections(name) {
        // Make request to the backend API
        const request = {
            name: name,
        };
        const fullRequest = {
            method: 'POST',
            body: JSON.stringify(request)
        };
        (0,_handler__WEBPACK_IMPORTED_MODULE_8__.requestAPI)(this._search_collection_type_url, fullRequest)
            .then((objectArray) => {
            if (JSON.stringify(objectArray) == JSON.stringify(this._objectArray)) {
                return;
            }
            // Update internal variable
            this._objectArray = objectArray;
            this._tableState.collections_array = objectArray;
            // Send signal for table widget to update data
            this._valueChanged.emit(this._tableState);
        });
    }
    get_search_placeholder() {
        return this._search_placeholder;
    }
}
/**
   * Insert WIPP Collection path code into editor
   */
function insertInputPath(editor, collection_path) {
    const cursor = editor.getCursorPosition();
    const offset = editor.getOffsetAt(cursor);
    const code = `input_path = ${collection_path}`;
    editor.model.value.insert(offset, code);
}
/**
 * Get the currently focused editor in the application,
 * checking both notebooks and consoles.
 * In the case of a notebook, it creates a new cell above the currently
 * active cell and then returns that.
 */
function getCurrentEditor(app, notebookTracker, consoleTracker) {
    // Get a handle on the most relevant editor,
    // whether it is attached to a notebook or a console.
    let current = app.shell.currentWidget;
    let editor;
    if (current && notebookTracker.has(current)) { //when editing notebook
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.insertAbove(current.content);
        const cell = current.content.activeCell;
        if (cell) {
            cell.model.metadata.set('tags', ["parameters"]); //set special metadata for Notebook executor plugin
        }
        editor = cell && cell.editor;
    }
    else if (current && consoleTracker.has(current)) { //when using code console
        const cell = current.console.promptCell;
        editor = cell && cell.editor;
    }
    return editor;
}


/***/ }),

/***/ "./lib/wippRegister.js":
/*!*****************************!*\
  !*** ./lib/wippRegister.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "WippRegister": () => (/* binding */ WippRegister)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");



class WippRegister extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
   * Instantiates the dialog and makes call to WIPP API.
   */
    constructor(path, name, description, openInWipp) {
        super();
        // Copy variables
        this.path = path;
        this.name = name;
        this.description = description;
        this.openInWipp = openInWipp;
        // Create dialog body
        this.body = this.createBody();
        this.node.appendChild(this.body);
        // Add spinner to show while requesting API
        this.spinner = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Spinner();
        this.node.appendChild(this.spinner.node);
        // Make API request
        this.registerNotebook();
    }
    /**
     * Executes the backend service API to register notebook in WIPP and handles response and errors.
     */
    registerNotebook() {
        // Make request to the backend API
        var request = {
            path: this.path,
            name: this.name,
            description: this.description
        };
        var fullRequest = {
            method: 'POST',
            body: JSON.stringify(request)
        };
        (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)('register', fullRequest)
            .then(response => {
            this.handleResponse(response);
        })
            .catch(() => this.handleError());
    }
    handleResponse(response) {
        // Remove spinner from dialog
        this.node.removeChild(this.spinner.node);
        this.spinner.dispose();
        // Throw exception for API error
        if (response.code !== 200) {
            this.handleError(response.error);
        }
        else {
            this.handleSuccess();
        }
        const info = response.info;
        // Open registered notebook in WIPP
        if (this.openInWipp) {
            window.open(info.url + info.id, '_blank');
        }
    }
    handleSuccess() {
        const label = document.createElement('label');
        const text = document.createElement('span');
        text.textContent = `Notebook '${this.name}' successfully registered in WIPP`;
        label.appendChild(text);
        this.body.appendChild(label);
    }
    handleError(message = 'Unexpected failure. Please check your Jupyter server logs for more details.') {
        const label = document.createElement('label');
        const text = document.createElement('span');
        text.textContent = `Notebook '${this.name}' registering in WIPP failed with error:`;
        const errorMessage = document.createElement('span');
        errorMessage.textContent = message;
        errorMessage.setAttribute('style', 'background-color:var(--jp-rendermime-error-background)');
        label.appendChild(text);
        label.appendChild(document.createElement('p'));
        label.appendChild(errorMessage);
        this.body.appendChild(label);
    }
    createBody() {
        const node = document.createElement('div');
        node.className = 'jp-RedirectForm';
        return node;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.bec80ddcb75e3fa21a51.js.map