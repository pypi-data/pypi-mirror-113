Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var debugImage_1 = require("app/types/debugImage");
function ProcessingIcon(_a) {
    var processingInfo = _a.processingInfo;
    switch (processingInfo.status) {
        case debugImage_1.CandidateProcessingStatus.OK:
            return <icons_1.IconCheckmark color="green300" size="xs"/>;
        case debugImage_1.CandidateProcessingStatus.ERROR: {
            var details = processingInfo.details;
            return (<tooltip_1.default title={details} disabled={!details}>
          <icons_1.IconClose color="red300" size="xs"/>
        </tooltip_1.default>);
        }
        case debugImage_1.CandidateProcessingStatus.MALFORMED: {
            var details = processingInfo.details;
            return (<tooltip_1.default title={details} disabled={!details}>
          <icons_1.IconWarning color="yellow300" size="xs"/>
        </tooltip_1.default>);
        }
        default: {
            Sentry.withScope(function (scope) {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate ProcessingIcon status'));
            });
            return null; // this shall never happen
        }
    }
}
exports.default = ProcessingIcon;
//# sourceMappingURL=processingIcon.jsx.map