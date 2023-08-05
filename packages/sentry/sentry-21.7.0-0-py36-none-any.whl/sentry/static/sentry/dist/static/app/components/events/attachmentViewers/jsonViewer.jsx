Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var contextData_1 = tslib_1.__importDefault(require("app/components/contextData"));
var previewPanelItem_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/previewPanelItem"));
var utils_1 = require("app/components/events/attachmentViewers/utils");
var JsonViewer = /** @class */ (function (_super) {
    tslib_1.__extends(JsonViewer, _super);
    function JsonViewer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    JsonViewer.prototype.getEndpoints = function () {
        return [['attachmentJson', utils_1.getAttachmentUrl(this.props)]];
    };
    JsonViewer.prototype.renderBody = function () {
        var attachmentJson = this.state.attachmentJson;
        if (!attachmentJson) {
            return null;
        }
        var json;
        try {
            json = JSON.parse(attachmentJson);
        }
        catch (e) {
            json = null;
        }
        return (<previewPanelItem_1.default>
        <StyledContextData data={json} maxDefaultDepth={4} preserveQuotes style={{ width: '100%' }} jsonConsts/>
      </previewPanelItem_1.default>);
    };
    return JsonViewer;
}(asyncComponent_1.default));
exports.default = JsonViewer;
var StyledContextData = styled_1.default(contextData_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=jsonViewer.jsx.map