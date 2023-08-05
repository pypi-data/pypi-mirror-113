Object.defineProperty(exports, "__esModule", { value: true });
exports.ADD_WIDGET_BUTTON_DRAG_ID = void 0;
var tslib_1 = require("tslib");
var sortable_1 = require("@dnd-kit/sortable");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var types_1 = require("./types");
var widgetWrapper_1 = tslib_1.__importDefault(require("./widgetWrapper"));
exports.ADD_WIDGET_BUTTON_DRAG_ID = 'add-widget-button';
var initialStyles = {
    x: 0,
    y: 0,
    scaleX: 1,
    scaleY: 1,
};
function AddWidget(_a) {
    var onAddWidget = _a.onAddWidget, onOpenWidgetBuilder = _a.onOpenWidgetBuilder, orgFeatures = _a.orgFeatures;
    var onClick = orgFeatures.includes('metrics') ? onOpenWidgetBuilder : onAddWidget;
    var _b = sortable_1.useSortable({
        disabled: true,
        id: exports.ADD_WIDGET_BUTTON_DRAG_ID,
        transition: null,
    }), setNodeRef = _b.setNodeRef, transform = _b.transform;
    return (<widgetWrapper_1.default key="add" ref={setNodeRef} displayType={types_1.DisplayType.BIG_NUMBER} layoutId={exports.ADD_WIDGET_BUTTON_DRAG_ID} style={{ originX: 0, originY: 0 }} animate={transform
            ? {
                x: transform.x,
                y: transform.y,
                scaleX: (transform === null || transform === void 0 ? void 0 : transform.scaleX) && transform.scaleX <= 1 ? transform.scaleX : 1,
                scaleY: (transform === null || transform === void 0 ? void 0 : transform.scaleY) && transform.scaleY <= 1 ? transform.scaleY : 1,
            }
            : initialStyles} transition={{
            duration: 0.25,
        }}>
      <InnerWrapper onClick={onClick}>
        <AddButton data-test-id="widget-add" onClick={onClick} icon={<icons_1.IconAdd size="lg" isCircled color="inactive"/>}/>
      </InnerWrapper>
    </widgetWrapper_1.default>);
}
exports.default = AddWidget;
var AddButton = styled_1.default(button_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border: none;\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    background: transparent;\n    box-shadow: none;\n  }\n"], ["\n  border: none;\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    background: transparent;\n    box-shadow: none;\n  }\n"])));
var InnerWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n  height: 110px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: ", ";\n"], ["\n  width: 100%;\n  height: 110px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return (p.onClick ? 'pointer' : ''); });
var templateObject_1, templateObject_2;
//# sourceMappingURL=addWidget.jsx.map