Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var locale_1 = require("app/locale");
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var editRulesModal_1 = tslib_1.__importDefault(require("app/views/settings/project/projectOwnership/editRulesModal"));
var EditOwnershipRulesModal = function (_a) {
    var Body = _a.Body, Header = _a.Header, onSave = _a.onSave, props = tslib_1.__rest(_a, ["Body", "Header", "onSave"]);
    return (<react_1.Fragment>
      <Header closeButton>{locale_1.t('Edit Ownership Rules')}</Header>
      <Body>
        <editRulesModal_1.default {...props} onSave={onSave}/>
      </Body>
    </react_1.Fragment>);
};
exports.modalCss = react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  @media (min-width: ", ") {\n    width: 80%;\n  }\n  [role='document'] {\n    overflow: initial;\n  }\n"], ["\n  @media (min-width: ", ") {\n    width: 80%;\n  }\n  [role='document'] {\n    overflow: initial;\n  }\n"])), theme_1.default.breakpoints[0]);
exports.default = EditOwnershipRulesModal;
var templateObject_1;
//# sourceMappingURL=editOwnershipRulesModal.jsx.map