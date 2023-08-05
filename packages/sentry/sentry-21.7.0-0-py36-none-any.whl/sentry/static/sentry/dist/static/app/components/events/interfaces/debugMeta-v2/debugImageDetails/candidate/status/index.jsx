Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var locale_1 = require("app/locale");
var debugImage_1 = require("app/types/debugImage");
function Status(_a) {
    var status = _a.status;
    switch (status) {
        case debugImage_1.CandidateDownloadStatus.OK: {
            return <tag_1.default type="success">{locale_1.t('Ok')}</tag_1.default>;
        }
        case debugImage_1.CandidateDownloadStatus.ERROR:
        case debugImage_1.CandidateDownloadStatus.MALFORMED: {
            return <tag_1.default type="error">{locale_1.t('Failed')}</tag_1.default>;
        }
        case debugImage_1.CandidateDownloadStatus.NOT_FOUND: {
            return <tag_1.default>{locale_1.t('Not Found')}</tag_1.default>;
        }
        case debugImage_1.CandidateDownloadStatus.NO_PERMISSION: {
            return <tag_1.default type="highlight">{locale_1.t('Permissions')}</tag_1.default>;
        }
        case debugImage_1.CandidateDownloadStatus.DELETED: {
            return <tag_1.default type="success">{locale_1.t('Deleted')}</tag_1.default>;
        }
        case debugImage_1.CandidateDownloadStatus.UNAPPLIED: {
            return <tag_1.default type="warning">{locale_1.t('Unapplied')}</tag_1.default>;
        }
        default: {
            Sentry.withScope(function (scope) {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate download status'));
            });
            return <tag_1.default>{locale_1.t('Unknown')}</tag_1.default>; // This shall not happen
        }
    }
}
exports.default = Status;
//# sourceMappingURL=index.jsx.map