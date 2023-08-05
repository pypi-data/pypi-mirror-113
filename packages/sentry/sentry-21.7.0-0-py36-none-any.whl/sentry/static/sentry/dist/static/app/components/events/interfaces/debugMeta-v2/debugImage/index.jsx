Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var layout_1 = tslib_1.__importDefault(require("../layout"));
var utils_1 = require("../utils");
var processings_1 = tslib_1.__importDefault(require("./processings"));
var status_1 = tslib_1.__importDefault(require("./status"));
function DebugImage(_a) {
    var image = _a.image, onOpenImageDetailsModal = _a.onOpenImageDetailsModal, style = _a.style;
    var unwind_status = image.unwind_status, debug_status = image.debug_status, debug_file = image.debug_file, debug_id = image.debug_id, code_file = image.code_file, code_id = image.code_id, status = image.status;
    var codeFilename = utils_1.getFileName(code_file);
    var debugFilename = utils_1.getFileName(debug_file);
    var imageAddress = utils_1.getImageAddress(image);
    return (<Wrapper style={style}>
      <StatusColumn>
        <status_1.default status={status}/>
      </StatusColumn>
      <ImageColumn>
        <div>
          {codeFilename && (<FileName>
              <tooltip_1.default title={code_file}>{codeFilename}</tooltip_1.default>
            </FileName>)}
          {codeFilename !== debugFilename && debugFilename && (<CodeFilename>{"(" + debugFilename + ")"}</CodeFilename>)}
        </div>
        {imageAddress && <ImageAddress>{imageAddress}</ImageAddress>}
      </ImageColumn>
      <Column>
        {unwind_status || debug_status ? (<processings_1.default unwind_status={unwind_status} debug_status={debug_status}/>) : (<notAvailable_1.default />)}
      </Column>
      <DebugFilesColumn>
        <button_1.default size="xsmall" onClick={function () { return onOpenImageDetailsModal(code_id, debug_id); }}>
          {locale_1.t('View')}
        </button_1.default>
      </DebugFilesColumn>
    </Wrapper>);
}
exports.default = DebugImage;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  :not(:last-child) {\n    > * {\n      border-bottom: 1px solid ", ";\n    }\n  }\n  ", ";\n"], ["\n  :not(:last-child) {\n    > * {\n      border-bottom: 1px solid ", ";\n    }\n  }\n  ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return layout_1.default(p.theme); });
var Column = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  display: flex;\n  align-items: center;\n"], ["\n  padding: ", ";\n  display: flex;\n  align-items: center;\n"])), space_1.default(2));
var StatusColumn = styled_1.default(Column)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  max-width: 100%;\n  overflow: hidden;\n"], ["\n  max-width: 100%;\n  overflow: hidden;\n"])));
var FileName = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-family: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"], ["\n  color: ", ";\n  font-family: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.text.family; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(0.5));
var CodeFilename = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var ImageColumn = styled_1.default(Column)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"], ["\n  font-family: ", ";\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; });
var ImageAddress = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-word;\n"], ["\n  white-space: pre-wrap;\n  word-break: break-word;\n"])));
var DebugFilesColumn = styled_1.default(Column)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=index.jsx.map