define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
    , 'nbextensions/visualpython/src/common/component/vpVarSelector'
    , 'nbextensions/visualpython/src/common/kernelApi'

    , 'codemirror/lib/codemirror'
    , 'codemirror/mode/python/python'
    , 'notebook/js/codemirror-ipython'
    , 'codemirror/addon/display/placeholder'
    , 'codemirror/addon/display/autorefresh'
], function (requirejs, $
    
            , vpConst, sb, vpCommon, vpSuggestInputText, pdGen, vpVarSelector, kernelApi
            
            , codemirror) {

    const VP_FE_BTN = 'vp-fe-btn';

    const VP_FE = 'vp-fe';
    const VP_FE_CONTAINER = 'vp-fe-container';
    const VP_FE_TITLE = 'vp-fe-title';
    const VP_FE_CLOSE = 'vp-fe-close';
    const VP_FE_BODY = 'vp-fe-body';

    const VP_FE_PREVIEW = 'vp-fe-preview';

    const VP_FE_DF_BOX = 'vp-fe-df-box';
    const VP_FE_DF_REFRESH = 'vp-fe-df-refresh';
    const VP_FE_DF_SHOWINFO = 'vp-fe-df-showinfo';

    const VP_FE_MENU_BOX = 'vp-fe-menu-box';
    const VP_FE_MENU_ITEM = 'vp-fe-menu-item';
    const VP_FE_MENU_SUB_BOX = 'vp-fe-menu-sub-box';

    const VP_FE_POPUP_BOX = 'vp-fe-popup-box';
    const VP_FE_POPUP_CLOSE = 'vp-fe-popup-close';
    const VP_FE_POPUP_BODY = 'vp-fe-popup-body';
    const VP_FE_POPUP_BUTTON_BOX = 'vp-fe-popup-button-box';
    const VP_FE_POPUP_CANCEL = 'vp-fe-popup-cancel';
    const VP_FE_POPUP_OK = 'vp-fe-popup-ok';

    const VP_FE_TABLE = 'vp-fe-table';
    const VP_FE_TABLE_COLUMN = 'vp-fe-table-column';
    const VP_FE_TABLE_ROW = 'vp-fe-table-row';
    const VP_FE_ADD_COLUMN = 'vp-fe-add-column';
    const VP_FE_ADD_ROW = 'vp-fe-add-row';
    const VP_FE_TABLE_MORE = 'vp-fe-table-more';

    const VP_FE_INFO = 'vp-fe-info';
    const VP_FE_INFO_TITLE = 'vp-fe-info-title';
    const VP_FE_INFO_CONTENT = 'vp-fe-info-content';

    const VP_FE_INFO_ERROR_BOX = 'vp-fe-info-error-box';
    const VP_FE_INFO_ERROR_BOX_TITLE = 'vp-fe-info-error-box-title';

    const VP_FE_PREVIEW_BOX = 'vp-fe-preview-box';
    const VP_FE_BUTTON_BOX = 'vp-fe-btn-box';
    const VP_FE_BUTTON_PREVIEW = 'vp-fe-btn-preview';
    const VP_FE_BUTTON_CANCEL = 'vp-fe-btn-cancel';
    const VP_FE_BUTTON_RUNADD = 'vp-fe-btn-runadd';
    const VP_FE_BUTTON_RUN = 'vp-fe-btn-run';
    const VP_FE_BUTTON_DETAIL = 'vp-fe-btn-detail';
    const VP_FE_DETAIL_BOX = 'vp-fe-detail-box';
    const VP_FE_DETAIL_ITEM = 'vp-fe-detail-item';
    // const VP_FE_BUTTON_BOX = 'vp-fe-btn-box';
    // const VP_FE_BUTTON_CANCEL = 'vp-fe-btn-cancel';
    // const VP_FE_BUTTON_APPLY = 'vp-fe-btn-apply';

    // search rows count at once
    const TABLE_LINES = 10;

    const FRAME_EDIT_TYPE = {
        NONE: -1,
        INIT: 0,

        RENAME: 2,
        DROP: 3,
        DROP_NA: 4,
        DROP_DUP: 5,
        ONE_HOT_ENCODING: 6,
        SET_IDX: 7,
        RESET_IDX: 8,
        REPLACE: 9,

        ADD_COL: 97,
        ADD_ROW: 98,
        SHOW: 99
    }

    /**
     * @class FrameEditor
     * @param {object} pageThis
     * @param {string} targetId
     * @constructor
     */
    var FrameEditor = function(pageThis, targetId) {
        this.pageThis = pageThis;
        this.targetId = targetId;
        this.uuid = 'u' + vpCommon.getUUID();

        this.renderButton();

        var that = this;
        // open popup
        $(vpCommon.formatString('.{0}.{1}', VP_FE_BTN, this.uuid)).on('click', function(event) {
            if (!$(this).hasClass('disabled')) {
                that.open();
            }
        });
    }

    FrameEditor.prototype.wrapSelector = function(query = '') {
        return vpCommon.formatString('.{0}.{1} {2}', VP_FE, this.uuid, query);
    }

    FrameEditor.prototype.open = function() {
        this.init();
        $(this.wrapSelector()).show();

        if (!this.codepreview) {
            // var previewTextarea = $('#vp_previewCode')[0];
            // var previewTextarea = $(this.wrapSelector('#vp_previewCode'))[0];
            var previewTextarea = $(this.wrapSelector('textarea'))[0];
            // if (!previewTextarea) {
            //     previewTextarea = $('#vp_previewCode')[0];
            // }
            if (previewTextarea) {
                // set codemirror
                this.codepreview = codemirror.fromTextArea(previewTextarea, {
                    mode: {
                        name: 'python',
                        version: 3,
                        singleLineStringErrors: false
                    },  // text-cell(markdown cell) set to 'htmlmixed'
                    height: '100%',
                    width: '100%',
                    indentUnit: 4,
                    matchBrackets: true,
                    readOnly:true,
                    autoRefresh: true,
                    // lineWrapping: true, // text-cell(markdown cell) set to true
                    // indentWithTabs: true,
                    theme: "ipython",
                    extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList"},
                    scrollbarStyle: "null"
                });
                this.setPreview('# Code Preview');
                this.codepreview.refresh();
            }
        } else {
            this.codepreview.refresh();
        }

        if (!this.cmpreviewall) {
            // codemirror setting
            this.cmpreviewall = codemirror.fromTextArea($('#vp_codePreview')[0], {
                mode: {
                    name: 'python',
                    version: 3,
                    singleLineStringErrors: false
                },  // text-cell(markdown cell) set to 'htmlmixed'
                height: '100%',
                width: '100%',
                indentUnit: 4,
                matchBrackets: true,
                readOnly:true,
                autoRefresh: true,
                theme: "ipython",
                extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList"},
                scrollbarStyle: "null"
            });
        } else {
            this.cmpreviewall.refresh();
        }
    }

    FrameEditor.prototype.close = function() {
        this.unbindEvent();
        $(this.wrapSelector()).remove();
    }

    FrameEditor.prototype.init = function() {
        // state
        this.state = {
            originObj: '',
            tempObj: '_vp',
            selected: [],
            axis: 0,
            lines: TABLE_LINES,
            steps: [],
            popup: {
                type: FRAME_EDIT_TYPE.NONE,
                replace: { index: 0 }
            }
        }

        this.codepreview = undefined;
        this.cmpreviewall = undefined;
        this.previewOpened = false;

        vpCommon.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "common/frameEditor.css");

        this.render();
        this.bindEvent();
        
        // this.setDraggableBox();
        this.setDraggableColumns();

        this.loadVariableList();
    }

    FrameEditor.prototype.initState = function() {
        this.state.selected = [];
        this.state.axis = -1;
        this.state.lines = TABLE_LINES;
        this.state.steps = [];
    }

    FrameEditor.prototype.renderButton = function() {
        // set button next to input tag
        var buttonTag = new sb.StringBuilder();
        buttonTag.appendFormat('<button type="button" class="{0} {1} {2}">{3}</button>'
                                , VP_FE_BTN, this.uuid, 'vp-button', 'Edit');
        if (this.pageThis) {
            $(this.pageThis.wrapSelector('#' + this.targetId)).parent().append(buttonTag.toString());
        }
    }

    FrameEditor.prototype.setPreview = function(previewCodeStr) {
        if (this.codepreview) {
            this.codepreview.setValue(previewCodeStr);
            this.codepreview.save();
            var that = this;
            setTimeout(function() {
                that.codepreview.refresh();
            }, 1);
        }
    }

    FrameEditor.prototype.render = function() {
        var page = new sb.StringBuilder();
        page.appendFormatLine('<div class="{0} {1}">', VP_FE, this.uuid);
        page.appendFormatLine('<div class="{0}">', VP_FE_CONTAINER);

        // menu box
        page.appendLine(this.renderMenuBox());
        // input popup
        page.appendLine(this.renderInputPopup());

        // title
        page.appendFormat('<div class="{0}">{1}</div>'
                            , VP_FE_TITLE
                            , 'Frame Editor');

        // close button
        page.appendFormatLine('<div class="{0}"><i class="{1}"></i></div>'
                                    , VP_FE_CLOSE, 'fa fa-close');

        // body start
        page.appendFormatLine('<div class="{0}">', VP_FE_BODY);

        // preview code board
        page.appendFormatLine('<div class="{0}"><textarea id="{1}" name="code"></textarea></div>'
                                , VP_FE_PREVIEW, "vp_fePreviewCode");

        // Select DataFrame
        page.appendFormatLine('<div class="{0}">', VP_FE_DF_BOX);
        page.appendFormatLine('<label for="{0}" class="{1}">{2}</label>', 'vp_feVariable', 'vp-orange-text', 'DataFrame');
        page.appendFormatLine('<select id="{0}">', 'vp_feVariable');
        page.appendLine('</select>');
        page.appendFormatLine('<i class="{0} {1}"></i>', VP_FE_DF_REFRESH, 'fa fa-refresh');
        page.appendFormatLine('<button class="{0} {1}"><i class="{2}"></i> View Info</button>', VP_FE_DF_SHOWINFO, 'vp-button', 'fa fa-columns');
        page.appendLine('</div>');

        // Table
        page.appendFormatLine('<div class="{0}">', VP_FE_TABLE);

        page.appendLine('</div>'); // End of Table

        page.appendLine('</div>'); // VP_FE_BODY
        
        // Info Box
        page.appendFormatLine('<div class="{0}">', VP_FE_INFO);
        page.appendFormatLine('<div class="{0}">Info</div>', VP_FE_INFO_TITLE);
        page.appendFormatLine('<div class="{0}">content</div>', VP_FE_INFO_CONTENT);
        page.appendLine('</div>'); // End of VP_FE_INFO


        // preview box
        page.appendFormatLine('<div class="{0} {1}">', VP_FE_PREVIEW_BOX, 'vp-apiblock-scrollbar');
        page.appendFormatLine('<textarea id="{0}" name="code"></textarea>', 'vp_codePreview');
        page.appendLine('</div>');

        // button box
        page.appendFormatLine('<div class="{0}">', VP_FE_BUTTON_BOX);
        page.appendFormatLine('<button type="button" class="{0} {1} {2}">{3}</button>'
                                , 'vp-button', 'vp-fe-btn', VP_FE_BUTTON_PREVIEW, 'Preview');
        page.appendFormatLine('<button type="button" class="{0} {1} {2}">{3}</button>'
                                , 'vp-button cancel', 'vp-fe-btn', VP_FE_BUTTON_CANCEL, 'Cancel');
        page.appendFormatLine('<div class="{0}">', VP_FE_BUTTON_RUNADD);
        page.appendFormatLine('<button type="button" class="{0} {1}">{2}</button>'
                                , 'vp-button activated', VP_FE_BUTTON_RUN, 'Run');
        page.appendFormatLine('<button type="button" class="{0} {1}"><i class="{2}"></i></button>'
                                , 'vp-button activated', VP_FE_BUTTON_DETAIL, 'fa fa-sort-up');
        page.appendFormatLine('<div class="{0} {1}">', VP_FE_DETAIL_BOX, 'vp-cursor');
        page.appendFormatLine('<div class="{0}" data-type="{1}">{2}</div>', VP_FE_DETAIL_ITEM, 'add', 'Add');
        page.appendLine('</div>'); // VP_FE_DETAIL_BOX
        page.appendLine('</div>'); // VP_FE_BUTTON_RUNADD
        page.appendLine('</div>'); // VP_FE_BUTTON_BOX
        // apply button
        // page.appendFormatLine('<div class="{0}">', VP_FE_BUTTON_BOX);
        // page.appendFormatLine('<button type="button" class="{0}">{1}</button>'
        //                         , VP_FE_BUTTON_CANCEL, 'Cancel');
        // page.appendFormatLine('<button type="button" class="{0}">{1}</button>'
        //                         , VP_FE_BUTTON_APPLY, 'Apply');
        // page.appendLine('</div>');

        page.appendLine('</div>'); // VP_FE_CONTAINER
        page.appendLine('</div>'); // VP_FE

        $('#vp-wrapper').append(page.toString());
        $(this.wrapSelector()).hide();
    }

    FrameEditor.prototype.renderMenuBox = function() {
        var page = new sb.StringBuilder();
        // Menus
        page.appendFormatLine('<div class="{0}" style="display:none; position: fixed;">', VP_FE_MENU_BOX);
        // menu 1. Add Column
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}" data-axis="{3}">{4}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-add-column', FRAME_EDIT_TYPE.ADD_COL, 'col', 'Add Column');
        // menu 2. Add Row
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}" data-axis="{3}">{4}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-add-row', FRAME_EDIT_TYPE.ADD_ROW, 'row', 'Add Row');
        // menu 3. drop
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}">{3}<i class="{4}" style="{5}"></i>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-drop', FRAME_EDIT_TYPE.DROP, 'Drop'
                            , 'fa fa-caret-right', 'padding-left: 5px;'); //TODO: NA & Duplicate selection needed
        // sub-menu 1.
        page.appendFormatLine('<div class="{0}" style="{1}">', VP_FE_MENU_SUB_BOX, 'top: 25px;');
        // menu 3-1. drop
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}">{3}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-drop', FRAME_EDIT_TYPE.DROP, 'Drop');
        // menu 3-2. drop-na
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}">{3}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-drop-na', FRAME_EDIT_TYPE.DROP_NA, 'Drop NA');
        // menu 3-3. drop-duplicate
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}" data-axis="{3}">{4}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-drop-duplicate', FRAME_EDIT_TYPE.DROP_DUP, 'col','Drop Duplicate');
        page.appendLine('</div>'); // end of sub-menu 1
        page.appendLine('</div>'); // end of menu 3
        // menu 4. rename
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}">{3}</div>'
                                                , VP_FE_MENU_ITEM, 'vp-fe-menu-rename', FRAME_EDIT_TYPE.RENAME, 'Rename');
        // menu 5. one-hot encoding
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}" data-axis="{3}">{4}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-ohe', FRAME_EDIT_TYPE.ONE_HOT_ENCODING, 'col', 'One-Hot Encoding');
        // menu 6. set index
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}" data-axis="{3}">{4}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-set-index', FRAME_EDIT_TYPE.SET_IDX, 'col', 'Set Index');
        // menu 6-2. reset index
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}" data-axis="{3}">{4}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-reset-index', FRAME_EDIT_TYPE.RESET_IDX, 'row', 'Reset Index');
        // menu 7. replace
        page.appendFormatLine('<div class="{0} {1}" data-type="{2}" data-axis="{3}">{4}</div>'
                            , VP_FE_MENU_ITEM, 'vp-fe-menu-replace', FRAME_EDIT_TYPE.REPLACE, 'col', 'Replace');
        page.appendLine('</div>'); // End of Menus
        return page.toString();
    }

    FrameEditor.prototype.renderInputPopup = function() {
        var page = new sb.StringBuilder();
        page.appendFormatLine('<div class="{0}" style="display: none;">', VP_FE_POPUP_BOX);
        // popup title
        page.appendFormat('<div class="{0}">{1}</div>'
                            , VP_FE_TITLE
                            , 'Input');
        // close button
        page.appendFormatLine('<div class="{0}"><i class="{1}"></i></div>'
                                    , VP_FE_POPUP_CLOSE, 'fa fa-close');
        page.appendFormatLine('<div class="{0}">', VP_FE_POPUP_BODY);



        page.appendLine('</div>'); // End of Body

        // apply button
        page.appendFormatLine('<div class="{0}">', VP_FE_POPUP_BUTTON_BOX);
        page.appendFormatLine('<button type="button" class="{0} {1}">{2}</button>'
                                , VP_FE_POPUP_CANCEL, 'vp-button cancel', 'Cancel');
        page.appendFormatLine('<button type="button" class="{0} {1}">{2}</button>'
                                , VP_FE_POPUP_OK, 'vp-button activated', 'OK');
        page.appendLine('</div>');

        page.appendLine('</div>'); // End of Popup
        return page.toString();
    }

    FrameEditor.prototype.loadVariableList = function() {
        var that = this;
        // load using kernel
        var dataTypes = ['DataFrame'];
        kernelApi.searchVarList(dataTypes, function(result) {
            try {
                var varList = JSON.parse(result);
                // render variable list
                // replace
                $(that.wrapSelector('#vp_feVariable')).replaceWith(function() {
                    return that.renderVariableList(varList);
                });
                $(that.wrapSelector('#vp_feVariable')).trigger('change');
            } catch (ex) {
                console.log('FrameEditor:', result);
                // console.log(ex);
            }
        });
    }

    FrameEditor.prototype.renderVariableList = function(varList) {
        var tag = new sb.StringBuilder();
        var beforeValue = $(this.wrapSelector('#vp_feVariable')).val();
        tag.appendFormatLine('<select id="{0}">', 'vp_feVariable');
        varList.forEach(vObj => {
            // varName, varType
            var label = vObj.varName;
            tag.appendFormatLine('<option value="{0}" data-type="{1}" {2}>{3}</option>'
                                , vObj.varName, vObj.varType
                                , beforeValue == vObj.varName?'selected':''
                                , label);
        });
        tag.appendLine('</select>'); // VP_VS_VARIABLES
        return tag.toString();
    }

    FrameEditor.prototype.renderTable = function(renderedText, isHtml=true) {
        var tag = new sb.StringBuilder();
        // Table
        tag.appendFormatLine('<div class="{0} {1} {2}">', VP_FE_TABLE, 'rendered_html', 'vp-apiblock-scrollbar');
        if (isHtml) {
            tag.appendFormatLine('<table class="dataframe">{0}</table>', renderedText);
            // More button
            tag.appendFormatLine('<div class="{0} {1}">More...</div>', VP_FE_TABLE_MORE, 'vp-button');
        } else {
            tag.appendFormatLine('<pre>{0}</pre>', renderedText);
        }
        tag.appendLine('</div>'); // End of Table
        return tag.toString();
    }

    FrameEditor.prototype.renderAddPage = function(type) {
        var content = new sb.StringBuilder();
        content.appendLine('<table><tr>');
        content.appendFormatLine('<th><label>New {0} name</label></th>', type);
        content.appendFormatLine('<td><input type="text" class="{0}"/>', 'vp-popup-input1');
        content.appendFormatLine('<label><input type="checkbox" class="{0}" checked/><span>{1}</span></label>', 'vp-popup-istext1','Text');
        content.appendLine('</td></tr><tr>');
        content.appendLine('<th><label>Value</label></th>');
        content.appendFormatLine('<td><input type="text" class="{0}"/>', 'vp-popup-input2');
        content.appendFormatLine('<label><input type="checkbox" class="{0}" checked/><span>{1}</span></label>', 'vp-popup-istext2','Text');
        content.appendLine('</td></tr></table>');
        return content.toString();
    }

    FrameEditor.prototype.renderRenamePage = function() {
        var content = new sb.StringBuilder();
        content.appendLine('<table>');
        this.state.selected.forEach((label, idx) => {
            content.appendLine('<tr>');
            content.appendFormatLine('<th><label>{0}</label></th>', label);
            content.appendFormatLine('<td><input type="text" class="{0}"/>', 'vp-popup-input' + idx);
            content.appendFormatLine('<label><input type="checkbox" class="{0}" checked/><span>{1}</span></label>', 'vp-popup-istext' + idx, 'Text');
            content.appendLine('</tr>');
        });
        content.appendLine('</table>');
        return content.toString();
    }

    FrameEditor.prototype.renderReplacePage = function() {
        var content = new sb.StringBuilder();
        content.appendFormatLine('<table class="{0}">', 'vp-popup-replace-table');
        content.appendLine(this.renderReplaceInput(0));
        content.appendFormatLine('<tr><td colspan="3"><button class="{0} {1}">{2}</button></td></tr>', 'vp-button', 'vp-popup-replace-add', '+ Add Key');
        content.appendLine('</table>');
        return content.toString();
    }

    FrameEditor.prototype.renderReplaceInput = function(index) {
        var content = new sb.StringBuilder();
        content.appendLine('<tr>');
        content.appendLine('<td>');
        content.appendFormatLine('<input type="text" class="{0}" placeholder="{1}"/>', 'vp-popup-origin' + index, 'origin');
        content.appendFormatLine('<label><input type="checkbox" class="{0}" checked/><span>{1}</span></label>', 'vp-popup-origin-istext' + index, 'Text');
        content.appendLine('</td>');
        content.appendLine('<td>');
        content.appendFormatLine('<input type="text" class="{0}" placeholder="{1}"/>', 'vp-popup-replace' + index, 'replace');
        content.appendFormatLine('<label><input type="checkbox" class="{0}" checked/><span>{1}</span></label>', 'vp-popup-replace-istext' + index, 'Text');
        content.appendLine('</td>');
        content.appendFormatLine('<td><i class="{0} {1} {2}"></i></td>', 'vp-popup-delete', 'fa fa-close', 'vp-cursor');
        content.appendLine('</tr>');
        return content.toString();
    }

    FrameEditor.prototype.openInputPopup = function(type, width=0, height=0) {
        var title = '';
        var content = '';

        switch (parseInt(type)) {
            case FRAME_EDIT_TYPE.ADD_COL:
                title = 'Add Column';
                content = this.renderAddPage('column');
                break;
            case FRAME_EDIT_TYPE.ADD_ROW:
                title = 'Add Row';
                content = this.renderAddPage('row');
                break;
            case FRAME_EDIT_TYPE.RENAME:
                title = 'Rename';
                content = this.renderRenamePage();
                break;
            case FRAME_EDIT_TYPE.REPLACE:
                title = 'Replace';
                content = this.renderReplacePage();
                break;
            default:
                type = FRAME_EDIT_TYPE.NONE;
                break;
        }

        this.state.popup.type = type;

        // set title
        $(this.wrapSelector('.' + VP_FE_POPUP_BOX + ' .' + VP_FE_TITLE)).text(title);
        // set content
        $(this.wrapSelector('.' + VP_FE_POPUP_BODY)).html(content);

        // show popup box
        $(this.wrapSelector('.' + VP_FE_POPUP_BOX)).show();
    }

    FrameEditor.prototype.getPopupContent = function() {
        var type = this.state.popup.type;
        var content = {};
        switch (parseInt(type)) {
            case FRAME_EDIT_TYPE.ADD_COL:
                content['name'] = $(this.wrapSelector('.vp-popup-input1')).val();
                content['nameastext'] = $(this.wrapSelector('.vp-popup-istext1')).prop('checked');
                content['value'] = $(this.wrapSelector('.vp-popup-input2')).val();
                content['valueastext'] = $(this.wrapSelector('.vp-popup-istext2')).prop('checked');
                break;
            case FRAME_EDIT_TYPE.ADD_ROW:
                content['name'] = $(this.wrapSelector('.vp-popup-input1')).val();
                content['nameastext'] = $(this.wrapSelector('.vp-popup-istext1')).prop('checked');
                content['value'] = $(this.wrapSelector('.vp-popup-input2')).val();
                content['valueastext'] = $(this.wrapSelector('.vp-popup-istext2')).prop('checked');
                break;
            case FRAME_EDIT_TYPE.RENAME:
                this.state.selected.forEach((label, idx) => {
                    var value = $(this.wrapSelector('.vp-popup-input'+idx)).val();
                    var istext = $(this.wrapSelector('.vp-popup-istext'+idx)).prop('checked');
                    content[idx] = {
                        label: label,
                        value: value,
                        istext: istext
                    };
                });
                break;
            case FRAME_EDIT_TYPE.REPLACE:
                var idx = 0;
                for (var i=0; i <= this.state.popup.replace.index; i++) {
                    var origin = $(this.wrapSelector('.vp-popup-origin' + i)).val();
                    var origintext = $(this.wrapSelector('.vp-popup-origin-istext'+idx)).prop('checked');
                    var replace = $(this.wrapSelector('.vp-popup-replace' + i)).val();
                    var replacetext = $(this.wrapSelector('.vp-popup-replace-istext'+idx)).prop('checked');
                    if (origin && replace) {
                        content[idx++] = {
                            origin: origin,
                            origintext: origintext,
                            replace: replace,
                            replacetext: replacetext
                        }
                    }
                }
                break;
            default:
                break;
        }
        return content;
    }

    FrameEditor.prototype.closeInputPopup = function() {
        $(this.wrapSelector('.' + VP_FE_POPUP_BOX)).hide();
    }

    /** open preview box */
    FrameEditor.prototype.openPreview = function() {
        var code = this.state.steps.join('\n');
        this.cmpreviewall.setValue(code);
        this.cmpreviewall.save();
        this.cmpreviewall.focus();

        var that = this;
        setTimeout(function() {
            that.cmpreviewall.refresh();
        },1);

        this.previewOpened = true;
        $(this.wrapSelector('.' + VP_FE_PREVIEW_BOX)).show();
    }

    /** close preview box */
    FrameEditor.prototype.closePreview = function() {
        this.previewOpened = false;
        $(this.wrapSelector('.' + VP_FE_PREVIEW_BOX)).hide();
    }

    FrameEditor.prototype.setDraggableBox = function() {
        $('.' + VP_FE_POPUP_BOX).draggable({
            containment: '.' + VP_FE_BODY
        });
    }

    FrameEditor.prototype.setDraggableColumns = function() {
        
    }

    FrameEditor.prototype.showInfo = function() {
        $(this.wrapSelector('.' + VP_FE_INFO)).show();
    }

    FrameEditor.prototype.hideInfo = function() {
        $(this.wrapSelector('.' + VP_FE_INFO)).hide();
    }

    FrameEditor.prototype.renderInfoPage = function(renderedText, isHtml = true) {
        var tag = new sb.StringBuilder();
        tag.appendFormatLine('<div class="{0} {1}">', VP_FE_INFO_CONTENT
                            , 'rendered_html'); // 'rendered_html' style from jupyter output area
        if (isHtml) {
            tag.appendLine(renderedText);
        } else {
            tag.appendFormatLine('<pre>{0}</pre>', renderedText);
        }
        tag.appendLine('</div>');
        return tag.toString();
    }

    FrameEditor.prototype.loadInfo = function() {
        var that = this;

        // get selected columns/indexes
        var selected = [];
        $(this.wrapSelector('.' + VP_FE_TABLE + ' th.selected')).each((idx, tag) => {
            var name = $(tag).data('label');
            selected.push(name);
        });
        this.state.selected = selected;

        var code = new sb.StringBuilder();
        var locObj = new sb.StringBuilder();
        locObj.appendFormat("{0}", this.state.tempObj);
        if (this.state.selected != '') {
            var rowCode = ':';
            var colCode = ':';
            if (this.state.axis == 0) {
                rowCode = '[' + this.state.selected.join(',') + ']';
            }
            if (this.state.axis == 1) {
                colCode = '[' + this.state.selected.join(',') + ']';
            }
            locObj.appendFormat(".loc[{0},{1}]", rowCode, colCode);
        }
        // code.append(".value_counts()");
        code.appendFormat('_vp_display_dataframe_info({0})', locObj.toString());
        
        // kernelApi.executePython(code.toString(), function(result) {
        //     $(that.wrapSelector('.' + VP_FE_INFO_CONTENT)).replaceWith(function() {
        //         // return vpCommon.formatString('<div class="{0}"><pre>{1}</pre></div>', VP_FE_INFO_CONTENT, result);
        //         return vpCommon.formatString('<div class="{0}">{1}</div>', VP_FE_INFO_CONTENT, result);
        //     });
        // }); 

        Jupyter.notebook.kernel.execute(
            code.toString(),
            {
                iopub: {
                    output: function(msg) {
                        if (msg.content.data) {
                            var htmlText = String(msg.content.data["text/html"]);
                            var codeText = String(msg.content.data["text/plain"]);
                            if (htmlText != 'undefined') {
                                $(that.wrapSelector('.' + VP_FE_INFO_CONTENT)).replaceWith(function() {
                                    return that.renderInfoPage(htmlText);
                                });
                            } else if (codeText != 'undefined') {
                                // plain text as code
                                $(that.wrapSelector('.' + VP_FE_INFO_CONTENT)).replaceWith(function() {
                                    return that.renderInfoPage(codeText, false);
                                });
                            } else {
                                $(that.wrapSelector('.' + VP_FE_INFO_CONTENT)).replaceWith(function() {
                                    return that.renderInfoPage('');
                                });
                            }
                        } else {
                            var errorContent = new sb.StringBuilder();
                            if (msg.content.ename) {
                                errorContent.appendFormatLine('<div class="{0}">', VP_FE_INFO_ERROR_BOX);
                                errorContent.appendLine('<i class="fa fa-exclamation-triangle"></i>');
                                errorContent.appendFormatLine('<label class="{0}">{1}</label>'
                                                            , VP_FE_INFO_ERROR_BOX_TITLE, msg.content.ename);
                                if (msg.content.evalue) {
                                    // errorContent.appendLine('<br/>');
                                    errorContent.appendFormatLine('<pre>{0}</pre>', msg.content.evalue.split('\\n').join('<br/>'));
                                }
                                errorContent.appendLine('</div>');
                            }
                            $(that.wrapSelector('.' + VP_FE_INFO_CONTENT)).replaceWith(function() {
                                return that.renderInfoPage(errorContent);
                            });
                        }
                    }
                }
            },
            { silent: false, store_history: true, stop_on_error: true }
        );
    }

    FrameEditor.prototype.getTypeCode = function(type, content={}) {
        var tempObj = this.state.tempObj;
        var orgObj = this.state.originObj;

        if (!orgObj || orgObj == '') {
            // object not selected

            return '';
        }

        var selectedName = this.state.selected.join(',');
        var axis = this.state.axis;

        var code = new sb.StringBuilder();
        switch (parseInt(type)) {
            case FRAME_EDIT_TYPE.INIT:
                code.appendFormat('{0} = {1}.copy()', tempObj, orgObj);
                break;
            case FRAME_EDIT_TYPE.DROP:
                code.appendFormat("{0}.drop([{1}], axis={2}, inplace=True)", tempObj, selectedName, axis);
                break;
            case FRAME_EDIT_TYPE.RENAME:
                var renameStr = new sb.StringBuilder();
                Object.keys(content).forEach((key, idx) => {
                    if (idx == 0) {
                        renameStr.appendFormat("{0}: {1}", content[key].label, convertToStr(content[key].value, content[key].istext));
                    } else {
                        renameStr.appendFormat(", {0}: {1}", content[key].label, convertToStr(content[key].value, content[key].istext));
                    }
                });
                code.appendFormat("{0}.rename({1}={{2}}, inplace=True)", tempObj, axis==0?'index':'columns', renameStr.toString());
                break;
            case FRAME_EDIT_TYPE.DROP_NA:
                var locObj = '';
                if (axis == 0) {
                    locObj = vpCommon.formatString('.loc[[{0}],:]', selectedName);
                } else {
                    locObj = vpCommon.formatString('.loc[:,[{0}]]', selectedName);
                }
                code.appendFormat("{0}{1}.dropna(axis={2}, inplace=True)", tempObj, locObj, axis);
                break;
            case FRAME_EDIT_TYPE.DROP_DUP:
                if (axis == 1) {
                    code.appendFormat("{0}.drop_duplicates(subset=[{1}], inplace=True)", tempObj, selectedName);
                }
                break;
            case FRAME_EDIT_TYPE.ONE_HOT_ENCODING:
                if (axis == 1) {
                    code.appendFormat("{0} = pd.get_dummies(data={1}, columns=[{2}])", tempObj, tempObj, selectedName);
                }
                break;
            case FRAME_EDIT_TYPE.SET_IDX:
                if (axis == 1) {
                    code.appendFormat("{0}.set_index([{1}], inplace=True)", tempObj, selectedName);
                }
                break;
            case FRAME_EDIT_TYPE.RESET_IDX:
                if (axis == 0) {
                    code.appendFormat("{0}.reset_index(inplace=True)", tempObj);
                }
                break;
            case FRAME_EDIT_TYPE.REPLACE:
                var replaceStr = new sb.StringBuilder();
                Object.keys(content).forEach((key, idx) => {
                    if (idx == 0) {
                        replaceStr.appendFormat("{0}: {1}"
                                                , convertToStr(content[key].origin, content[key].origintext)
                                                , convertToStr(content[key].replace, content[key].replacetext));
                    } else {
                        replaceStr.appendFormat(", {0}: {1}"
                                                , convertToStr(content[key].origin, content[key].origintext)
                                                , convertToStr(content[key].replace, content[key].replacetext));
                    }
                });

                // var locObj = '';
                // if (axis == 0) {
                //     locObj = vpCommon.formatString('.loc[[{0}],:]', selectedName);
                // } else {
                //     locObj = vpCommon.formatString('.loc[:,[{0}]]', selectedName);
                // }
                code.appendFormat("{0}[[{1}]] = {2}[[{3}]].replace({{4}})", tempObj, selectedName, tempObj, selectedName, replaceStr);
                break;
            case FRAME_EDIT_TYPE.ADD_COL:
                var name = convertToStr(content.name, content.nameastext);
                var value = convertToStr(content.value, content.valueastext);
                code.appendFormat("{0}[{1}] = {2}", tempObj, name, value);
                break;
            case FRAME_EDIT_TYPE.ADD_ROW: 
                var name = convertToStr(content.name, content.nameastext);
                var value = convertToStr(content.value, content.valueastext);
                code.appendFormat("{0}.loc[{1}] = {2}", tempObj, name, value);
                break;
            case FRAME_EDIT_TYPE.SHOW:
                break;
        }

        return code.toString();
    }
    
    FrameEditor.prototype.loadCode = function(codeStr) {
        var that = this;

        if (code == '') {
            return ;
        }

        var tempObj = this.state.tempObj;
        var lines = this.state.lines;

        var code = new sb.StringBuilder();
        code.appendLine(codeStr);
        code.appendFormat("{0}.head({1}).to_json(orient='{2}')", tempObj, lines, 'split');
        console.log(code.toString());
        kernelApi.executePython(code.toString(), function(result) {
            try {
                var data = JSON.parse(result.substr(1,result.length - 2).replaceAll('\\\\', '\\'));
                console.log(data);
                var columnList = data.columns;
                var indexList = data.index;
                var dataList = data.data;

                // table
                var table = new sb.StringBuilder();
                // table.appendFormatLine('<table border="{0}" class="{1}">', 1, 'dataframe');
                table.appendLine('<thead>');
                table.appendLine('<tr><th></th>');
                columnList && columnList.forEach(col => {
                    var colLabel = convertToStr(col, typeof col == 'string');
                    var colClass = '';
                    if (that.state.axis == 1 && that.state.selected.includes(colLabel)) {
                        colClass = 'selected';
                    }
                    table.appendFormatLine('<th data-label="{0}" data-axis="{1}" class="{2} {3}">{4}</th>', colLabel, 1, VP_FE_TABLE_COLUMN, colClass, col);
                });
                // add column
                table.appendFormatLine('<th class="{0}"><i class="{1}"></i></th>', VP_FE_ADD_COLUMN, 'fa fa-plus');

                table.appendLine('</tr>');
                table.appendLine('</thead>');
                table.appendLine('<tbody>');

                dataList && dataList.forEach((row, idx) => {
                    table.appendLine('<tr>');
                    var idxName = indexList[idx];
                    var idxLabel = convertToStr(idxName, typeof idxName == 'string');
                    var idxClass = '';
                    if (that.state.axis == 0 && that.state.selected.includes(idxLabel)) {
                        idxClass = 'selected';
                    }
                    table.appendFormatLine('<th data-label="{0}" data-axis="{1}" class="{2} {3}">{4}</th>', idxLabel, 0, VP_FE_TABLE_ROW, idxClass, idxName);
                    row.forEach(cell => {
                        if (cell == null) {
                            cell = 'NaN';
                        }
                        table.appendFormatLine('<td>{0}</td>', cell);
                    });
                    // empty data
                    // table.appendLine('<td></td>');
                    table.appendLine('</tr>');
                });
                // add row
                table.appendLine('<tr>');
                table.appendFormatLine('<th class="{0}"><i class="{1}"></i></th>', VP_FE_ADD_ROW, 'fa fa-plus');
                table.appendLine('</tbody>');
                table.appendLine('</tr>');
                $(that.wrapSelector('.' + VP_FE_TABLE)).replaceWith(function() {
                    return that.renderTable(table.toString());
                });
                // load info
                that.loadInfo();
                // add to stack
                if (codeStr !== '') {
                    that.state.steps.push(codeStr);
                    that.setPreview(codeStr);
                }
            } catch (err) {
                console.log(err);
            }
        });
    }

    FrameEditor.prototype.apply = function(runCell = true) {
        var code = this.state.steps.join('\n');
        if (this.pageThis) {
            $(this.pageThis.wrapSelector('#' + this.targetId)).val(code);
            $(this.pageThis.wrapSelector('#' + this.targetId)).trigger({
                type: 'frame_run',
                code: code,
                runCell: runCell
            });
        } else {
            $(vpCommon.wrapSelector('#' + this.targetId)).val(code);
            $(vpCommon.wrapSelector('#' + this.targetId)).trigger({
                type: 'frame_run',
                code: code,
                runCell: runCell
            });
        }
    }

    FrameEditor.prototype.unbindEvent = function() {
        $(document).off(this.wrapSelector('*'));

        $(document).off('click', this.wrapSelector('.' + VP_FE_CLOSE));
        $(document).off('change', this.wrapSelector('#vp_feVariable'));
        $(document).off('click', this.wrapSelector('.vp-fe-df-refresh'));
        $(document).off('click', this.wrapSelector('.vp-fe-df-showinfo'));
        $(document).off('click', this.wrapSelector('.' + VP_FE_INFO));
        $(document).off('contextmenu', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_COLUMN));
        $(document).off('contextmenu', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_ROW));
        $(document).off('click', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_COLUMN));
        $(document).off('click', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_ROW));
        $(document).off('click', this.wrapSelector('.' + VP_FE_ADD_COLUMN));
        $(document).off('click', this.wrapSelector('.' + VP_FE_ADD_ROW));
        $(document).off('click', this.wrapSelector('.' + VP_FE_TABLE_MORE));
        $(document).off('click', this.wrapSelector('.' + VP_FE_MENU_ITEM));
        $(document).off('click', this.wrapSelector('.' + VP_FE_POPUP_OK));
        $(document).off('click', this.wrapSelector('.' + VP_FE_POPUP_CANCEL));
        $(document).off('click', this.wrapSelector('.' + VP_FE_POPUP_CLOSE));
        $(document).off('click', this.wrapSelector('.' + VP_FE_BUTTON_PREVIEW));
        $(document).off('click', this.wrapSelector('.' + VP_FE_BUTTON_CANCEL));
        $(document).off('click', this.wrapSelector('.' + VP_FE_BUTTON_RUN));
        $(document).off('click', this.wrapSelector('.' + VP_FE_BUTTON_DETAIL));
        $(document).off('click', this.wrapSelector('.' + VP_FE_DETAIL_ITEM));
        $(document).off('click.' + this.uuid);

    }

    FrameEditor.prototype.bindEvent = function() {
        var that = this;
        
        // close popup
        $(document).on('click', this.wrapSelector('.' + VP_FE_CLOSE), function(event) {
            that.close();

            $(vpCommon.formatString('.{0}.{1}', VP_FE_BTN, this.uuid)).remove();
            // vpCommon.removeHeadScript("vpSubsetEditor");
        });

        // select df
        $(document).on('change', this.wrapSelector('#vp_feVariable'), function() {
            // set temporary df
            var origin = $(this).val();

            // initialize state values
            that.state.originObj = origin;
            that.state.tempObj = '_vp';
            that.initState();

            // load code with temporary df
            that.loadCode(that.getTypeCode(FRAME_EDIT_TYPE.INIT));
            that.loadInfo();
        });

        // refresh df
        $(document).on('click', this.wrapSelector('.vp-fe-df-refresh'), function() {
            that.loadVariableList();
        });

        // show info
        $(document).on('click', this.wrapSelector('.vp-fe-df-showinfo'), function() {
            that.showInfo();
        });

        $(document).on('click', this.wrapSelector('.' + VP_FE_INFO), function(evt) {
            evt.stopPropagation();
        });

        // menu on column
        $(document).on('contextmenu', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_COLUMN), function(event) {
            event.preventDefault();
            var hasSelected = $(this).hasClass('selected');
            $(that.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_ROW)).removeClass('selected');
            // select col/idx
            if (!hasSelected) {
                $(this).addClass('selected');
                var newAxis = $(this).data('axis');
                that.state.axis = newAxis;
            }

            that.loadInfo();

            // show menu
            var thisPos = $(this).position();
            var thisRect = $(this)[0].getBoundingClientRect();
            that.showMenu(thisPos.left, thisPos.top + thisRect.height);
        });

        // menu on row
        $(document).on('contextmenu', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_ROW), function(event) {
            event.preventDefault();
            var hasSelected = $(this).hasClass('selected');
            $(that.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_COLUMN)).removeClass('selected');
            // select col/idx
            if (!hasSelected) {
                $(this).addClass('selected');
                var newAxis = $(this).data('axis');
                that.state.axis = newAxis;
            }

            that.loadInfo();

            // show menu
            var thisPos = $(this).position();
            var thisRect = $(this)[0].getBoundingClientRect();
            var tblPos = $(that.wrapSelector('.' + VP_FE_TABLE)).position();
            that.showMenu(tblPos.left + thisRect.width, tblPos.top + thisPos.top);
        });

        // hide menu
        $(document).on('click', function(evt) {
            if (evt.target.id != 'vp_apiblock_menu_box') {
                // close menu
                that.hideMenu();
            }
            if (!$(evt.target).hasClass(VP_FE_DF_SHOWINFO)) {
                // close info
                that.hideInfo();
            }
        });

        // select column
        $(document).on('click', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_COLUMN), function(evt) {
            evt.stopPropagation();
            var hasSelected = $(this).hasClass('selected');
            $(that.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_ROW)).removeClass('selected');
            if (!hasSelected) {
                $(this).addClass('selected');
                var newAxis = $(this).data('axis');
                that.state.axis = newAxis;
            } else {
                $(this).removeClass('selected');
            }
            
            that.loadInfo();
        });

        // select row
        $(document).on('click', this.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_ROW), function() {
            var hasSelected = $(this).hasClass('selected');
            $(that.wrapSelector('.' + VP_FE_TABLE + ' .' + VP_FE_TABLE_COLUMN)).removeClass('selected');
            if (!hasSelected) {
                $(this).addClass('selected');
                var newAxis = $(this).data('axis');
                that.state.axis = newAxis;
            } else {
                $(this).removeClass('selected');
            }
            
            that.loadInfo();
        });

        // add column
        $(document).on('click', this.wrapSelector('.' + VP_FE_ADD_COLUMN), function() {
            // add column
            that.openInputPopup(FRAME_EDIT_TYPE.ADD_COL);
        });

        // add row
        $(document).on('click', this.wrapSelector('.' + VP_FE_ADD_ROW), function() {
            // add row
            that.openInputPopup(FRAME_EDIT_TYPE.ADD_ROW);
        });

        // more rows
        $(document).on('click', this.wrapSelector('.' + VP_FE_TABLE_MORE), function() {
            that.state.lines += TABLE_LINES;
            that.loadCode(that.getTypeCode(FRAME_EDIT_TYPE.SHOW));
        });

        // click menu item
        $(document).on('click', this.wrapSelector('.' + VP_FE_MENU_ITEM), function(event) {
            event.stopPropagation();
            var editType = $(this).data('type');
            switch (parseInt(editType)) {
                case FRAME_EDIT_TYPE.ADD_COL:
                case FRAME_EDIT_TYPE.ADD_ROW:
                case FRAME_EDIT_TYPE.RENAME:
                case FRAME_EDIT_TYPE.REPLACE:
                    that.openInputPopup(editType);
                    break;
                default:
                    that.loadCode(that.getTypeCode(editType));
                    break;
            }
            that.hideMenu();
        });

        // popup : replace - add button
        $(document).on('click', this.wrapSelector('.vp-popup-replace-add'), function() {
            var newInput = $(that.renderReplaceInput(++that.state.popup.replace.index));
            newInput.insertBefore(
                $(that.wrapSelector('.vp-popup-replace-table tr:last'))
            );
        });

        // popup : replace - delete row
        $(document).on('click', this.wrapSelector('.vp-popup-delete'), function() {
            $(this).closest('tr').remove();
        });

        // ok input popup
        $(document).on('click', this.wrapSelector('.' + VP_FE_POPUP_OK), function() {
            // ok input popup
            that.loadCode(that.getTypeCode(that.state.popup.type, that.getPopupContent()));
            that.closeInputPopup();
        });

        // cancel input popup
        $(document).on('click', this.wrapSelector('.' + VP_FE_POPUP_CANCEL), function() {
            that.closeInputPopup();
        });

        // close input popup
        $(document).on('click', this.wrapSelector('.' + VP_FE_POPUP_CLOSE), function() {
            that.closeInputPopup();
        });

        // click preview
        $(document).on('click', this.wrapSelector('.' + VP_FE_BUTTON_PREVIEW), function(evt) {
            evt.stopPropagation();
            if (that.previewOpened) {
                that.closePreview();
            } else {
                that.openPreview();
            }
        });

        // click cancel
        $(document).on('click', this.wrapSelector('.' + VP_FE_BUTTON_CANCEL), function() {
            that.close();
        });

        // click run
        $(document).on('click', this.wrapSelector('.' + VP_FE_BUTTON_RUN), function() {
            that.apply();
            that.close();
        });

        // click detail button
        $(document).on('click', this.wrapSelector('.' + VP_FE_BUTTON_DETAIL), function(evt) {
            evt.stopPropagation();
            $(that.wrapSelector('.' + VP_FE_DETAIL_BOX)).show();
        });

        // click add
        $(document).on('click', this.wrapSelector('.' + VP_FE_DETAIL_ITEM), function() {
            var type = $(this).data('type');
            if (type == 'add') {
                that.apply(false);
                that.close();
            }
        });

        // click other
        $(document).on('click.' + this.uuid, function(evt) {
            if (!$(evt.target).hasClass('.' + VP_FE_BUTTON_DETAIL)) {
                $(that.wrapSelector('.' + VP_FE_DETAIL_BOX)).hide();
            }
            if (!$(evt.target).hasClass('.' + VP_FE_BUTTON_PREVIEW)
                && $(that.wrapSelector('.' + VP_FE_PREVIEW_BOX)).has(evt.target).length === 0) {
                that.closePreview();
            }
        });
    }

    FrameEditor.prototype.showMenu = function(left, top) {
        if (this.state.axis == 0) {
            // row
            $(this.wrapSelector(vpCommon.formatString('.{0}', VP_FE_MENU_BOX))).find('div[data-axis="col"]').hide();
            $(this.wrapSelector(vpCommon.formatString('.{0}', VP_FE_MENU_BOX))).find('div[data-axis="row"]').show();
        } else if (this.state.axis == 1) {
            // column
            $(this.wrapSelector(vpCommon.formatString('.{0}', VP_FE_MENU_BOX))).find('div[data-axis="row"]').hide();
            $(this.wrapSelector(vpCommon.formatString('.{0}', VP_FE_MENU_BOX))).find('div[data-axis="col"]').show();
        }
        $(this.wrapSelector(vpCommon.formatString('.{0}', VP_FE_MENU_BOX))).css({ top: top, left: left })
        $(this.wrapSelector(vpCommon.formatString('.{0}', VP_FE_MENU_BOX))).show();
    }

    FrameEditor.prototype.hideMenu = function() {
        $(this.wrapSelector(vpCommon.formatString('.{0}', VP_FE_MENU_BOX))).hide();
    }

    var convertToStr = function(code, isText) {
        if (isText) {
            code = "'" + code + "'";
        }
        return code;
    }

    return FrameEditor;
});