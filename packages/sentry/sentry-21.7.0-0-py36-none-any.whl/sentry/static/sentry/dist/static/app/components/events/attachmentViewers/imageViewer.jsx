Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/components/events/attachmentViewers/utils");
var panels_1 = require("app/components/panels");
function ImageViewer(_a) {
    var className = _a.className, props = tslib_1.__rest(_a, ["className"]);
    return (<Container className={className}>
      <img src={utils_1.getAttachmentUrl(props, true)}/>
    </Container>);
}
exports.default = ImageViewer;
var Container = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  justify-content: center;\n"], ["\n  justify-content: center;\n"])));
var templateObject_1;
//# sourceMappingURL=imageViewer.jsx.map