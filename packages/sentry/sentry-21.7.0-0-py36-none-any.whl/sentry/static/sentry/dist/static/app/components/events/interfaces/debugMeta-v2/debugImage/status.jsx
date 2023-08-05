Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var locale_1 = require("app/locale");
var debugImage_1 = require("app/types/debugImage");
function Status(_a) {
    var status = _a.status;
    switch (status) {
        case debugImage_1.ImageStatus.OTHER:
        case debugImage_1.ImageStatus.FETCHING_FAILED:
        case debugImage_1.ImageStatus.MALFORMED:
        case debugImage_1.ImageStatus.TIMEOUT: {
            return <StyledTag type="error">{locale_1.t('Error')}</StyledTag>;
        }
        case debugImage_1.ImageStatus.MISSING: {
            return <StyledTag type="error">{locale_1.t('Missing')}</StyledTag>;
        }
        case debugImage_1.ImageStatus.FOUND: {
            return <StyledTag type="success">{locale_1.t('Ok')}</StyledTag>;
        }
        case debugImage_1.ImageStatus.UNUSED: {
            return <StyledTag>{locale_1.t('Unreferenced')}</StyledTag>;
        }
        default: {
            Sentry.withScope(function (scope) {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image status'));
            });
            return <StyledTag>{locale_1.t('Unknown')}</StyledTag>; // This shall not happen
        }
    }
}
exports.default = Status;
var StyledTag = styled_1.default(tag_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  &,\n  span div {\n    max-width: 100%;\n  }\n"], ["\n  &,\n  span div {\n    max-width: 100%;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=status.jsx.map