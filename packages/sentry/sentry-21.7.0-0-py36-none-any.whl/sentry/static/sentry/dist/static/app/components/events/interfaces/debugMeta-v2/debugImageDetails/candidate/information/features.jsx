Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var debugImage_1 = require("app/types/debugImage");
var utils_1 = require("../utils");
function Features(_a) {
    var download = _a.download;
    var features = [];
    if (download.status === debugImage_1.CandidateDownloadStatus.OK ||
        download.status === debugImage_1.CandidateDownloadStatus.DELETED ||
        download.status === debugImage_1.CandidateDownloadStatus.UNAPPLIED) {
        features = Object.keys(download.features).filter(function (feature) { return download.features[feature]; });
    }
    return (<react_1.Fragment>
      {Object.keys(debugImage_1.ImageFeature).map(function (imageFeature) {
            var _a = utils_1.getImageFeatureDescription(imageFeature), label = _a.label, description = _a.description;
            var isDisabled = !features.includes(imageFeature);
            return (<StyledTag key={label} disabled={isDisabled} tooltipText={isDisabled ? undefined : description}>
            {label}
          </StyledTag>);
        })}
    </react_1.Fragment>);
}
exports.default = Features;
var StyledTag = styled_1.default(tag_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  opacity: ", ";\n"], ["\n  opacity: ", ";\n"])), function (p) { return (p.disabled ? '0.35' : 1); });
var templateObject_1;
//# sourceMappingURL=features.jsx.map