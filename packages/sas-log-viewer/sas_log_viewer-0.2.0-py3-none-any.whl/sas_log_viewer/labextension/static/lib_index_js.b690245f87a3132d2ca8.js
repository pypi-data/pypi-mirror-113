(self["webpackChunksas_log_viewer"] = self["webpackChunksas_log_viewer"] || []).push([["lib_index_js"],{

/***/ "./lib/iconImport.js":
/*!***************************!*\
  !*** ./lib/iconImport.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "sasLogIcon": () => (/* binding */ sasLogIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_Jupyter_Log_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/Jupyter_Log.svg */ "./style/icons/Jupyter_Log.svg?966e");


const sasLogIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'custom-ui-components:sasLog',
    svgstr: _style_icons_Jupyter_Log_svg__WEBPACK_IMPORTED_MODULE_1__.default
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
/* harmony export */   "ISASLogExtension": () => (/* binding */ ISASLogExtension),
/* harmony export */   "saslogExtension": () => (/* binding */ saslogExtension),
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
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");










/**
 * IDs of the commands added by this extension.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.newSASlog = 'saslog:new';
})(CommandIDs || (CommandIDs = {}));
/**
 * The token identifying the JupyterLab plugin.
 */
const ISASLogExtension = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.Token('jupyter.extensions.saslog');
const saslogProp = new _lumino_properties__WEBPACK_IMPORTED_MODULE_7__.AttachedProperty({
    create: () => '',
    name: 'SASLogTarget'
});
class saslogExtension {
    /**
     *
     */
    constructor(commands) {
        this.commands = commands;
    }
    /**
     * Create a new extension object.
     */
    createNew(nb, context) {
        // Add buttons to toolbar
        const buttons = [];
        let insertionPoint = -1;
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_4__.find)(nb.toolbar.children(), (tbb, index) => {
            if (tbb.hasClass('jp-Notebook-toolbarCellType')) {
                insertionPoint = index;
                return true;
            }
            return false;
        });
        let i = 1;
        for (const id of [CommandIDs.newSASlog]) {
            const button = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButton({ id, commands: this.commands });
            button.addClass('jp-saslog-nbtoolbarbutton');
            if (insertionPoint >= 0) {
                nb.toolbar.insertItem(insertionPoint + i++, this.commands.label(id), button);
            }
            else {
                nb.toolbar.insertAfter('cellType', this.commands.label(id), button);
            }
            buttons.push(button);
        }
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_6__.DisposableDelegate(() => {
            // Cleanup extension here
            for (const btn of buttons) {
                btn.dispose();
            }
        });
    }
}
/**
 * Add the main file view commands to the application's command registry.
 */
function addCommands(app, tracker, saslogTracker, palette, menu) {
    const { commands, shell } = app;
    /**
     * Whether there is an active SAS notebook
     */
    function hasKernel() {
        var _a, _b, _c;
        return (tracker.currentWidget !== null &&
            ((_c = (_b = (_a = tracker.currentWidget.context.sessionContext) === null || _a === void 0 ? void 0 : _a.session) === null || _b === void 0 ? void 0 : _b.kernel) !== null && _c !== void 0 ? _c : null) !== null &&
            tracker.currentWidget.sessionContext.prevKernelName == 'sas');
    }
    commands.addCommand(CommandIDs.newSASlog, {
        label: 'Show SAS Log',
        caption: 'Show the SAS log for the associated notebook',
        iconClass: 'jp-Icon jp-Icon-16 jp-saslogIcon',
        isEnabled: hasKernel,
        execute: args => {
            var _a, _b, _c;
            let notebook;
            if (args.path) {
                notebook = (_a = tracker.find(nb => nb.context.path === args.path)) !== null && _a !== void 0 ? _a : null;
            }
            else {
                notebook = tracker.currentWidget;
            }
            if (!notebook) {
                return;
            }
            const widget = new _widget__WEBPACK_IMPORTED_MODULE_8__.SASLogView((_c = (_b = notebook.context.sessionContext) === null || _b === void 0 ? void 0 : _b.session) === null || _c === void 0 ? void 0 : _c.kernel);
            widget.title.label = `SAS Log: ${notebook.title.label}`;
            notebook.title.changed.connect(() => {
                widget.title.label = `SAS Log: ${notebook.title.label}`;
            });
            const outer = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: widget });
            saslogProp.set(widget, notebook.context.path);
            notebook.context.pathChanged.connect((_, path) => {
                saslogProp.set(widget, path);
                saslogTracker.save(outer);
            });
            saslogTracker.add(outer);
            notebook.context.sessionContext.kernelChanged.connect((_, args) => {
                widget.model.kernel = args.newValue;
            });
            shell.add(outer, 'main', { mode: 'split-right' });
            if (args['activate'] !== false) {
                shell.activateById(outer.id);
            }
            notebook.disposed.connect(() => {
                outer.close();
            });
        }
    });
    palette === null || palette === void 0 ? void 0 : palette.addItem({
        command: CommandIDs.newSASlog,
        category: 'Kernel'
    });
    menu === null || menu === void 0 ? void 0 : menu.kernelMenu.addGroup([{ command: CommandIDs.newSASlog }]);
}
/**
 * Initialization data for the jupyterlab-saslog extension.
 */
const extension = {
    id: 'sas-log-viewer:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: ISASLogExtension,
    activate: async (app, tracker, palette, mainMenu, restorer) => {
        console.log('SAS log_viewer extension is activated!');
        const { commands, docRegistry } = app;
        const extension = new saslogExtension(commands);
        docRegistry.addWidgetExtension('Notebook', extension);
        // Recreate views from layout restorer
        const saslogTracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'saslog'
        });
        if (restorer) {
            void restorer.restore(saslogTracker, {
                command: CommandIDs.newSASlog,
                args: widget => ({
                    path: saslogProp.get(widget.content),
                    activate: false
                }),
                name: widget => saslogProp.get(widget.content),
                when: tracker.restored
            });
        }
        addCommands(app, tracker, saslogTracker, palette, mainMenu);
        function refreshNewCommand() {
            commands.notifyCommandChanged(CommandIDs.newSASlog);
        }
        // Update the command registry when the notebook state changes.
        tracker.currentChanged.connect(refreshNewCommand);
        let prevWidget = tracker.currentWidget;
        if (prevWidget) {
            prevWidget.context.sessionContext.kernelChanged.connect(refreshNewCommand);
        }
        tracker.currentChanged.connect(tracker => {
            if (prevWidget) {
                prevWidget.context.sessionContext.kernelChanged.disconnect(refreshNewCommand);
            }
            prevWidget = tracker.currentWidget;
            if (prevWidget) {
                prevWidget.context.sessionContext.kernelChanged.connect(refreshNewCommand);
            }
        });
        return extension;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/model.js":
/*!**********************!*\
  !*** ./lib/model.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ThreadIterator": () => (/* binding */ ThreadIterator),
/* harmony export */   "SASLogModel": () => (/* binding */ SASLogModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);

const showLogCommand = '%showLog';
const executeRequestMsgType = 'execute_request';
const statusMsgType = 'status';
const idleExecutionState = 'idle';
function isHeader(candidate) {
    return candidate.msg_id !== undefined;
}
class ThreadIterator {
    constructor(threads, collapsed) {
        this._threads = threads;
        this._collapsed = collapsed;
        this._index = -1;
        this._child = null;
    }
    iter() {
        return this;
    }
    next() {
        if (this._child) {
            const next = this._child.next();
            if (next !== undefined) {
                return next;
            }
            this._child = null;
        }
        // Move to next thread
        ++this._index;
        if (this._index >= this._threads.length) {
            return undefined;
        }
        const entry = this._threads[this._index];
        if (entry.children.length > 0 &&
            !this._collapsed[entry.args.msg.header.msg_id]) {
            // Iterate over children after this
            this._child = new ThreadIterator(entry.children, this._collapsed);
        }
        return { args: entry.args, hasChildren: entry.children.length > 0 };
    }
    clone() {
        const r = new ThreadIterator(this._threads, this._collapsed);
        r._index = this._index;
        if (this._child) {
            r._child = this._child.clone();
        }
        return r;
    }
}
/**
 * Model for a SAS Log.
 */
class SASLogModel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
    constructor(kernel) {
        super();
        this.requestStarted = '';
        this.logRequestStarted = '';
        this.logStreamObj = {};
        this._log = [];
        this._kernel = null;
        this._messages = {};
        this._childLUT = {};
        this._roots = [];
        this.kernel = kernel !== null && kernel !== void 0 ? kernel : null;
    }
    clear() {
        this._log.splice(0, this._log.length);
        this._messages = {};
        this._childLUT = {};
        this._roots = [];
        this.logStreamObj = {};
        this.stateChanged.emit(void 0);
    }
    get kernel() {
        return this._kernel;
    }
    set kernel(value) {
        if (this._kernel) {
            this._kernel.anyMessage.disconnect(this.onMessage, this);
        }
        this._kernel = value;
        if (this._kernel) {
            this._kernel.anyMessage.connect(this.onMessage, this);
        }
    }
    get log() {
        return this._log;
    }
    get tree() {
        return this._roots.map(rootId => {
            return this.getThread(rootId, false);
        });
    }
    depth(args) {
        if (args === null) {
            return -1;
        }
        let depth = 0;
        while ((args = this._findParent(args))) {
            ++depth;
        }
        return depth;
    }
    getThread(msgId, ancestors = true) {
        const args = this._messages[msgId];
        if (ancestors) {
            // Work up to root, then work downwards
            let root = args;
            let candidate;
            while ((candidate = this._findParent(root))) {
                root = candidate;
            }
            return this.getThread(root.msg.header.msg_id, false);
        }
        const childMessages = this._childLUT[msgId] || [];
        const childThreads = childMessages.map(childId => {
            return this.getThread(childId, false);
        });
        const thread = {
            args: this._messages[msgId],
            children: childThreads
        };
        return thread;
    }
    onMessage(sender, args) {
        var _a, _b, _c, _d, _e;
        const { msg } = args;
        console.log(`%c ${msg.header.msg_type}`, 'color: purple; font-weight: bold; font-size: 14px;');
        console.log(msg.content);
        this._log.push(args);
        this._messages[msg.header.msg_id] = args;
        const parent = this._findParent(args);
        if (parent === null) {
            this._roots.push(msg.header.msg_id);
        }
        else {
            const header = parent.msg.header;
            this._childLUT[header.msg_id] = this._childLUT[header.msg_id] || [];
            this._childLUT[header.msg_id].push(msg.header.msg_id);
        }
        // Check if execute_request has started
        // @ts-ignore
        if (msg.header.msg_type === executeRequestMsgType && msg.content.code !== showLogCommand && !this.requestStarted) {
            this.requestStarted = msg.header.msg_id;
        }
        // Check if execute_request has ended
        const execRequestHasEnded = this.requestStarted &&
            // @ts-ignore
            ((_a = msg.parent_header) === null || _a === void 0 ? void 0 : _a.msg_id) === this.requestStarted &&
            // @ts-ignore
            msg.content.execution_state === idleExecutionState && msg.header.msg_type === statusMsgType;
        // If execute_request has finished run %showLog command
        if (execRequestHasEnded) {
            console.log('%c --------- showLog start -------', 'color: red; font-weight: bold;');
            // Fetch the log
            (_b = this.kernel) === null || _b === void 0 ? void 0 : _b.requestExecute({ code: showLogCommand }, true);
        }
        // @ts-ignore
        const isLogRequest = msg.header.msg_type === executeRequestMsgType && ((_c = msg.content) === null || _c === void 0 ? void 0 : _c.code) === showLogCommand;
        // If it's %showLog execute_request
        if (isLogRequest) {
            this.requestStarted = ''; // reset initial execute_request has started flag
            let id = msg.header.msg_id; // get msg_id
            this.logRequestStarted = id; // set logRequestStartedId so we can start tracking log streams that will come in future
            this.logStreamObj[id] = []; // create array in logStreamObj under msg_id key - this key is later used to identify stream msg.parent_header id
        }
        // If we have log request stared and msg_type is stream save it in logStreamsObj under parent_header msg_id key
        if (this.logRequestStarted && msg.header.msg_type === 'stream') {
            // @ts-ignore
            let id = (_d = msg.parent_header) === null || _d === void 0 ? void 0 : _d.msg_id;
            // @ts-ignore
            this.logStreamObj[id].push(msg.content.text);
        }
        // Check if %showLog has ended
        const logRequestHasEnded = this.logRequestStarted &&
            // @ts-ignore
            ((_e = msg.parent_header) === null || _e === void 0 ? void 0 : _e.msg_id) === this.logRequestStarted &&
            // @ts-ignore
            msg.content.execution_state === idleExecutionState && msg.header.msg_type === statusMsgType;
        // If status is Idle and logRequestsStarted this menas that %showLog command has finished
        // and logRequestStarted has to be cleared
        if (logRequestHasEnded && this.logRequestStarted) {
            console.log('%c --------- showLog end -------', 'color: red; font-weight: bold;');
            this.logRequestStarted = '';
        }
        this.stateChanged.emit(undefined);
    }
    _findParent(args) {
        if (isHeader(args.msg.parent_header)) {
            return this._messages[args.msg.parent_header.msg_id] || null;
        }
        return null;
    }
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MessageLogView": () => (/* binding */ MessageLogView),
/* harmony export */   "SASLogView": () => (/* binding */ SASLogView)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var ansi_to_html__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ansi-to-html */ "webpack/sharing/consume/default/ansi-to-html/ansi-to-html");
/* harmony import */ var ansi_to_html__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(ansi_to_html__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./model */ "./lib/model.js");
/* harmony import */ var _iconImport__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./iconImport */ "./lib/iconImport.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
/* harmony import */ var _style_widget_css__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/widget.css */ "./style/widget.css");











const convert = new (ansi_to_html__WEBPACK_IMPORTED_MODULE_5___default())();
/**
 * The main view for the SAS log viewer.
 */
class MessageLogView extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.VDomRenderer {
    constructor(model) {
        super(model);
        this.collapsedKeys = {};
        this.id = `saslog-messagelog-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.UUID.uuid4()}`;
        this.addClass('jp-saslog-messagelog');
    }
    /**
     * Render the extension discovery view using the virtual DOM.
     */
    render() {
        const logStreamObj = this.model.logStreamObj;
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null, Object.keys(logStreamObj).map((key) => {
            const collapsed = this.collapsedKeys[key];
            const collapserIcon = collapsed ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretRightIcon : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretDownIcon;
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { key: key, className: `collapsible ${collapsed ? 'collapsed' : ''}` },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'log-header' },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: `collapser`, onClick: () => {
                            this.collapsedKeys[key] = !this.collapsedKeys[key];
                            this.update();
                        } },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement(collapserIcon.react, { className: 'kspy-collapser-icon' })),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'log-id' }, key)),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'log-container' }, logStreamObj[key].map((stream, i) => react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { key: `${key}-${i}` },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { dangerouslySetInnerHTML: { __html: convert.toHtml(stream) } })))));
        })));
    }
    collapseAll() {
        for (const key in this.model.logStreamObj) {
            this.collapsedKeys[key] = true;
        }
        this.update();
    }
    expandAll() {
        this.collapsedKeys = {};
        this.update();
    }
}
/**
 * The main view for the SAS Log viewer.
 */
class SASLogView extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    constructor(kernel) {
        super();
        this._model = new _model__WEBPACK_IMPORTED_MODULE_8__.SASLogModel(kernel);
        this.addClass('jp-saslog-view');
        this.id = `saslog-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.UUID.uuid4()}`;
        this.title.label = 'SAS Log';
        this.title.closable = true;
        this.title.icon = _iconImport__WEBPACK_IMPORTED_MODULE_9__.sasLogIcon;
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.BoxLayout());
        this._toolbar = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Toolbar();
        this._toolbar.addClass('jp-saslog-toolbar');
        this._messagelog = new MessageLogView(this._model);
        layout.addWidget(this._toolbar);
        layout.addWidget(this._messagelog);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.BoxLayout.setStretch(this._toolbar, 0);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.BoxLayout.setStretch(this._messagelog, 1);
        this.collapseAllButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            onClick: () => {
                this._messagelog.collapseAll();
            },
            className: 'jp-saslog-collapseAll',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretRightIcon,
            tooltip: 'Collapse all threads'
        });
        this._toolbar.addItem('collapse-all', this.collapseAllButton);
        this.expandAllButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            onClick: () => {
                this._messagelog.expandAll();
            },
            className: 'jp-saslog-expandAll',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretDownIcon,
            tooltip: 'Expand all threads'
        });
        this._toolbar.addItem('expand-all', this.expandAllButton);
        this.clearAllButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            onClick: () => {
                this._model.clear();
            },
            className: 'jp-saslog-clearAll',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.closeIcon,
            tooltip: 'Clear all threads'
        });
        this._toolbar.addItem('clear-all', this.clearAllButton);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        if (!this.node.contains(document.activeElement)) {
            this.collapseAllButton.node.focus();
        }
    }
    get model() {
        return this._model;
    }
}


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__.default);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/widget.css":
/*!****************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/widget.css ***!
  \****************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, ".collapsible {\n    height: auto;\n    overflow: hidden;\n    transition: height 0.5s;\n    margin-bottom: 10px;\n    border-bottom: 1px solid lightgray;\n    padding-bottom: 6px;\n}\n\n.collapsible.collapsed {\n    height: 25px;\n}\n\n.log-header {\n    margin-bottom: 5px;\n}\n\n.log-header div.log-id {\n    display: inline-block;\n    margin-left: 15px;\n    font-weight: 600;\n}\n\n.log-container {\n    white-space: pre-wrap;\n}\n", "",{"version":3,"sources":["webpack://./style/widget.css"],"names":[],"mappings":"AAAA;IACI,YAAY;IACZ,gBAAgB;IAChB,uBAAuB;IACvB,mBAAmB;IACnB,kCAAkC;IAClC,mBAAmB;AACvB;;AAEA;IACI,YAAY;AAChB;;AAEA;IACI,kBAAkB;AACtB;;AAEA;IACI,qBAAqB;IACrB,iBAAiB;IACjB,gBAAgB;AACpB;;AAEA;IACI,qBAAqB;AACzB","sourcesContent":[".collapsible {\n    height: auto;\n    overflow: hidden;\n    transition: height 0.5s;\n    margin-bottom: 10px;\n    border-bottom: 1px solid lightgray;\n    padding-bottom: 6px;\n}\n\n.collapsible.collapsed {\n    height: 25px;\n}\n\n.log-header {\n    margin-bottom: 5px;\n}\n\n.log-header div.log-id {\n    display: inline-block;\n    margin-left: 15px;\n    font-weight: 600;\n}\n\n.log-container {\n    white-space: pre-wrap;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/icons/Jupyter_Log.svg?966e":
/*!*************************************!*\
  !*** ./style/icons/Jupyter_Log.svg ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<!-- Generator: Adobe Illustrator 24.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->\n<svg version=\"1.1\" id=\"Log\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" x=\"0px\" y=\"0px\"\n\t viewBox=\"0 0 16 16\" style=\"enable-background:new 0 0 16 16;\" xml:space=\"preserve\">\n<style type=\"text/css\">\n\t.st0{fill:none;}\n\t.st1{fill:#5D5D5D;}\n</style>\n<rect id=\"svgToolTipPane\" y=\"1\" class=\"st0\" width=\"14\" height=\"14\"/>\n<path id=\"iconColor\" class=\"st1\" d=\"M13,1H3C2.5,1,2,1.5,2,2v12c0,0.6,0.5,1,1,1h10c0.6,0,1-0.4,1-1V2C14,1.5,13.6,1,13,1z M13,14H3\n\tV3h10V14z M12,8H4V7h8V8z M12,5H4v1h8V5z M12,9H4v1h8V9z M12,11H4v1h8V11z\"/>\n</svg>\n");

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ }),

/***/ "./style/widget.css":
/*!**************************!*\
  !*** ./style/widget.css ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./style/widget.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__.default, options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_widget_css__WEBPACK_IMPORTED_MODULE_1__.default.locals || {});

/***/ })

}]);
//# sourceMappingURL=lib_index_js.b690245f87a3132d2ca8.js.map