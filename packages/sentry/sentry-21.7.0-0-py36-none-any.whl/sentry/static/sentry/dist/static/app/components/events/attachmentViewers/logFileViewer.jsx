Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var ansicolor_1 = tslib_1.__importDefault(require("ansicolor"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var previewPanelItem_1 = tslib_1.__importDefault(require("app/components/events/attachmentViewers/previewPanelItem"));
var utils_1 = require("app/components/events/attachmentViewers/utils");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var theme_1 = tslib_1.__importDefault(require("app/utils/theme"));
var COLORS = {
    black: theme_1.default.black,
    white: theme_1.default.white,
    redDim: theme_1.default.red200,
    red: theme_1.default.red300,
    greenDim: theme_1.default.green200,
    green: theme_1.default.green300,
    yellowDim: theme_1.default.yellow300,
    yellow: theme_1.default.orange300,
    blueDim: theme_1.default.blue200,
    blue: theme_1.default.blue300,
    magentaDim: theme_1.default.pink200,
    magenta: theme_1.default.pink300,
    cyanDim: theme_1.default.blue200,
    cyan: theme_1.default.blue300,
};
var LogFileViewer = /** @class */ (function (_super) {
    tslib_1.__extends(LogFileViewer, _super);
    function LogFileViewer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    LogFileViewer.prototype.getEndpoints = function () {
        return [['attachmentText', utils_1.getAttachmentUrl(this.props)]];
    };
    LogFileViewer.prototype.renderBody = function () {
        var attachmentText = this.state.attachmentText;
        if (!attachmentText) {
            return null;
        }
        var spans = ansicolor_1.default
            .parse(attachmentText)
            .spans.map(function (_a, idx) {
            var color = _a.color, bgColor = _a.bgColor, text = _a.text;
            var style = {};
            if (color) {
                if (color.name) {
                    style.color =
                        COLORS[color.name + (color.dim ? 'Dim' : '')] || COLORS[color.name] || '';
                }
                if (color.bright) {
                    style.fontWeight = 500;
                }
            }
            if (bgColor && bgColor.name) {
                style.background =
                    COLORS[bgColor.name + (bgColor.dim ? 'Dim' : '')] ||
                        COLORS[bgColor.name] ||
                        '';
            }
            return (<span style={style} key={idx}>
            {text}
          </span>);
        });
        return (<previewPanelItem_1.default>
        <CodeWrapper>{spans}</CodeWrapper>
      </previewPanelItem_1.default>);
    };
    return LogFileViewer;
}(asyncComponent_1.default));
exports.default = LogFileViewer;
var CodeWrapper = styled_1.default('pre')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", " ", ";\n  width: 100%;\n  margin-bottom: 0;\n  &:after {\n    content: '';\n  }\n"], ["\n  padding: ", " ", ";\n  width: 100%;\n  margin-bottom: 0;\n  &:after {\n    content: '';\n  }\n"])), space_1.default(1), space_1.default(2));
var templateObject_1;
//# sourceMappingURL=logFileViewer.jsx.map