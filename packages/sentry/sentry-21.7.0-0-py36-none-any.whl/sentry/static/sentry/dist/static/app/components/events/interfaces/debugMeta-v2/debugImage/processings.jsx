Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var item_1 = tslib_1.__importDefault(require("../processing/item"));
var list_1 = tslib_1.__importDefault(require("../processing/list"));
var processingIcon_1 = tslib_1.__importDefault(require("./processingIcon"));
function Processings(_a) {
    var unwind_status = _a.unwind_status, debug_status = _a.debug_status;
    var items = [];
    if (debug_status) {
        items.push(<StyledProcessingItem key="symbolication" type="symbolication" icon={<processingIcon_1.default status={debug_status}/>}/>);
    }
    if (unwind_status) {
        items.push(<StyledProcessingItem key="stack_unwinding" type="stack_unwinding" icon={<processingIcon_1.default status={unwind_status}/>}/>);
    }
    return <StyledProcessingList items={items}/>;
}
exports.default = Processings;
var StyledProcessingList = styled_1.default(list_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  margin-bottom: -", ";\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  margin-bottom: -", ";\n"])), space_1.default(1));
var StyledProcessingItem = styled_1.default(item_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  :not(:last-child) {\n    padding-right: ", ";\n  }\n  padding-bottom: ", ";\n"], ["\n  :not(:last-child) {\n    padding-right: ", ";\n  }\n  padding-bottom: ", ";\n"])), space_1.default(2), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=processings.jsx.map