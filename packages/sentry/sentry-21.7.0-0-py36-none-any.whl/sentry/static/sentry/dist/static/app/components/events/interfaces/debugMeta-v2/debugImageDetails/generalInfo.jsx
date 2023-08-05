Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var notAvailable_1 = tslib_1.__importDefault(require("app/components/notAvailable"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var processings_1 = tslib_1.__importDefault(require("../debugImage/processings"));
var utils_1 = require("../utils");
function GeneralInfo(_a) {
    var image = _a.image;
    var _b = image !== null && image !== void 0 ? image : {}, debug_id = _b.debug_id, debug_file = _b.debug_file, code_id = _b.code_id, code_file = _b.code_file, arch = _b.arch, unwind_status = _b.unwind_status, debug_status = _b.debug_status;
    var imageAddress = image ? utils_1.getImageAddress(image) : undefined;
    return (<Wrapper>
      <Label coloredBg>{locale_1.t('Address Range')}</Label>
      <Value coloredBg>{imageAddress !== null && imageAddress !== void 0 ? imageAddress : <notAvailable_1.default />}</Value>

      <Label>{locale_1.t('Debug ID')}</Label>
      <Value>{debug_id !== null && debug_id !== void 0 ? debug_id : <notAvailable_1.default />}</Value>

      <Label coloredBg>{locale_1.t('Debug File')}</Label>
      <Value coloredBg>{debug_file !== null && debug_file !== void 0 ? debug_file : <notAvailable_1.default />}</Value>

      <Label>{locale_1.t('Code ID')}</Label>
      <Value>{code_id !== null && code_id !== void 0 ? code_id : <notAvailable_1.default />}</Value>

      <Label coloredBg>{locale_1.t('Code File')}</Label>
      <Value coloredBg>{code_file !== null && code_file !== void 0 ? code_file : <notAvailable_1.default />}</Value>

      <Label>{locale_1.t('Architecture')}</Label>
      <Value>{arch !== null && arch !== void 0 ? arch : <notAvailable_1.default />}</Value>

      <Label coloredBg>{locale_1.t('Processing')}</Label>
      <Value coloredBg>
        {unwind_status || debug_status ? (<processings_1.default unwind_status={unwind_status} debug_status={debug_status}/>) : (<notAvailable_1.default />)}
      </Value>
    </Wrapper>);
}
exports.default = GeneralInfo;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"])));
var Label = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", " ", " ", ";\n  ", "\n"], ["\n  color: ", ";\n  padding: ", " ", " ", " ", ";\n  ", "\n"])), function (p) { return p.theme.textColor; }, space_1.default(1), space_1.default(1.5), space_1.default(1), space_1.default(1), function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; });
var Value = styled_1.default(Label)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-all;\n  color: ", ";\n  padding: ", ";\n  font-family: ", ";\n  ", "\n"], ["\n  white-space: pre-wrap;\n  word-break: break-all;\n  color: ", ";\n  padding: ", ";\n  font-family: ", ";\n  ", "\n"])), function (p) { return p.theme.subText; }, space_1.default(1), function (p) { return p.theme.text.familyMono; }, function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=generalInfo.jsx.map