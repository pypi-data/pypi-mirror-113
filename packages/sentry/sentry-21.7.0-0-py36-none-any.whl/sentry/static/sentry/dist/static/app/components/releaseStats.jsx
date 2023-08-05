Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var avatarList_1 = tslib_1.__importDefault(require("app/components/avatar/avatarList"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ReleaseStats = function (_a) {
    var release = _a.release, _b = _a.withHeading, withHeading = _b === void 0 ? true : _b;
    var commitCount = release.commitCount || 0;
    var authorCount = (release.authors && release.authors.length) || 0;
    if (commitCount === 0) {
        return null;
    }
    var releaseSummary = [
        locale_1.tn('%s commit', '%s commits', commitCount),
        locale_1.t('by'),
        locale_1.tn('%s author', '%s authors', authorCount),
    ].join(' ');
    return (<div className="release-stats">
      {withHeading && <ReleaseSummaryHeading>{releaseSummary}</ReleaseSummaryHeading>}
      <span style={{ display: 'inline-block' }}>
        <avatarList_1.default users={release.authors} avatarSize={25} typeMembers="authors"/>
      </span>
    </div>);
};
var ReleaseSummaryHeading = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.2;\n  font-weight: 600;\n  text-transform: uppercase;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; }, space_1.default(0.5));
exports.default = ReleaseStats;
var templateObject_1;
//# sourceMappingURL=releaseStats.jsx.map