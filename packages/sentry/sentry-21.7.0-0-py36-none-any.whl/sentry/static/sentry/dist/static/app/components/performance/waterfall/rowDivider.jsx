Object.defineProperty(exports, "__esModule", { value: true });
exports.EmbeddedTransactionBadge = exports.ErrorBadge = exports.DividerLineGhostContainer = exports.DividerLine = exports.DividerContainer = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var icons_1 = require("app/icons");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
exports.DividerContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  min-width: 1px;\n"], ["\n  position: relative;\n  min-width: 1px;\n"])));
exports.DividerLine = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n  position: absolute;\n  height: 100%;\n  width: 1px;\n  transition: background-color 125ms ease-in-out;\n  z-index: ", ";\n\n  /* enhanced hit-box */\n  &:after {\n    content: '';\n    z-index: -1;\n    position: absolute;\n    left: -2px;\n    top: 0;\n    width: 5px;\n    height: 100%;\n  }\n\n  &.hovering {\n    background-color: ", ";\n    width: 3px;\n    transform: translateX(-1px);\n    margin-right: -2px;\n\n    cursor: ew-resize;\n\n    &:after {\n      left: -2px;\n      width: 7px;\n    }\n  }\n"], ["\n  background-color: ", ";\n  position: absolute;\n  height: 100%;\n  width: 1px;\n  transition: background-color 125ms ease-in-out;\n  z-index: ", ";\n\n  /* enhanced hit-box */\n  &:after {\n    content: '';\n    z-index: -1;\n    position: absolute;\n    left: -2px;\n    top: 0;\n    width: 5px;\n    height: 100%;\n  }\n\n  &.hovering {\n    background-color: ", ";\n    width: 3px;\n    transform: translateX(-1px);\n    margin-right: -2px;\n\n    cursor: ew-resize;\n\n    &:after {\n      left: -2px;\n      width: 7px;\n    }\n  }\n"])), function (p) { return (p.showDetail ? p.theme.textColor : p.theme.border); }, function (p) { return p.theme.zIndex.traceView.dividerLine; }, function (p) { return p.theme.textColor; });
exports.DividerLineGhostContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  width: 100%;\n  height: 100%;\n"], ["\n  position: absolute;\n  width: 100%;\n  height: 100%;\n"])));
var BadgeBorder = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  margin: ", ";\n  left: -11px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border: 1px solid ", ";\n  border-radius: 50%;\n  z-index: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  position: absolute;\n  margin: ", ";\n  left: -11px;\n  background: ", ";\n  width: ", ";\n  height: ", ";\n  border: 1px solid ", ";\n  border-radius: 50%;\n  z-index: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])), space_1.default(0.25), function (p) { return p.theme.background; }, space_1.default(3), space_1.default(3), function (p) { return p.theme[p.borderColor]; }, function (p) { return p.theme.zIndex.traceView.dividerLine; });
function ErrorBadge() {
    return (<BadgeBorder borderColor="red300">
      <icons_1.IconFire color="red300" size="xs"/>
    </BadgeBorder>);
}
exports.ErrorBadge = ErrorBadge;
function EmbeddedTransactionBadge(_a) {
    var expanded = _a.expanded, onClick = _a.onClick;
    return (<BadgeBorder borderColor="border" onClick={function (event) {
            event.stopPropagation();
            event.preventDefault();
            onClick();
        }}>
      {expanded ? (<icons_1.IconSubtract color="textColor" size="xs"/>) : (<icons_1.IconAdd color="textColor" size="xs"/>)}
    </BadgeBorder>);
}
exports.EmbeddedTransactionBadge = EmbeddedTransactionBadge;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=rowDivider.jsx.map