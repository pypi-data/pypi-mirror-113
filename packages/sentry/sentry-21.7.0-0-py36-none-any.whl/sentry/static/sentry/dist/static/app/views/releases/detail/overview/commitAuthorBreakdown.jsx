Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var collapsible_1 = tslib_1.__importDefault(require("app/components/collapsible"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var formatters_1 = require("app/utils/formatters");
var styles_1 = require("./styles");
var CommitAuthorBreakdown = /** @class */ (function (_super) {
    tslib_1.__extends(CommitAuthorBreakdown, _super);
    function CommitAuthorBreakdown() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    CommitAuthorBreakdown.prototype.getEndpoints = function () {
        var _a = this.props, orgId = _a.orgId, projectSlug = _a.projectSlug, version = _a.version;
        var commitsEndpoint = "/projects/" + orgId + "/" + projectSlug + "/releases/" + encodeURIComponent(version) + "/commits/";
        return [['commits', commitsEndpoint]];
    };
    CommitAuthorBreakdown.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.version !== this.props.version) {
            this.remountComponent();
        }
    };
    CommitAuthorBreakdown.prototype.getDisplayPercent = function (authorCommitCount) {
        var commits = this.state.commits;
        var calculatedPercent = Math.round(utils_1.percent(authorCommitCount, commits.length));
        return (calculatedPercent < 1 ? '<1' : calculatedPercent) + "%";
    };
    CommitAuthorBreakdown.prototype.renderBody = function () {
        var _this = this;
        var _a;
        // group commits by author
        var groupedAuthorCommits = (_a = this.state.commits) === null || _a === void 0 ? void 0 : _a.reduce(function (authorCommitsAccumulator, commit) {
            var _a, _b;
            var email = (_b = (_a = commit.author) === null || _a === void 0 ? void 0 : _a.email) !== null && _b !== void 0 ? _b : 'unknown';
            if (authorCommitsAccumulator.hasOwnProperty(email)) {
                authorCommitsAccumulator[email].commitCount += 1;
            }
            else {
                authorCommitsAccumulator[email] = {
                    commitCount: 1,
                    author: commit.author,
                };
            }
            return authorCommitsAccumulator;
        }, {});
        // sort authors by number of commits
        var sortedAuthorsByNumberOfCommits = Object.values(groupedAuthorCommits).sort(function (a, b) { return b.commitCount - a.commitCount; });
        if (!sortedAuthorsByNumberOfCommits.length) {
            return null;
        }
        return (<styles_1.Wrapper>
        <styles_1.SectionHeading>{locale_1.t('Commit Author Breakdown')}</styles_1.SectionHeading>
        <collapsible_1.default expandButton={function (_a) {
                var onExpand = _a.onExpand, numberOfHiddenItems = _a.numberOfHiddenItems;
                return (<button_1.default priority="link" onClick={onExpand}>
              {locale_1.tn('Show %s collapsed author', 'Show %s collapsed authors', numberOfHiddenItems)}
            </button_1.default>);
            }}>
          {sortedAuthorsByNumberOfCommits.map(function (_a, index) {
                var _b;
                var commitCount = _a.commitCount, author = _a.author;
                return (<AuthorLine key={(_b = author === null || author === void 0 ? void 0 : author.email) !== null && _b !== void 0 ? _b : index}>
              <userAvatar_1.default user={author} size={20} hasTooltip/>
              <AuthorName>{formatters_1.userDisplayName(author || {}, false)}</AuthorName>
              <Commits>{locale_1.tn('%s commit', '%s commits', commitCount)}</Commits>
              <Percent>{_this.getDisplayPercent(commitCount)}</Percent>
            </AuthorLine>);
            })}
        </collapsible_1.default>
      </styles_1.Wrapper>);
    };
    return CommitAuthorBreakdown;
}(asyncComponent_1.default));
var AuthorLine = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: 30px 2fr 1fr 40px;\n  width: 100%;\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  display: inline-grid;\n  grid-template-columns: 30px 2fr 1fr 40px;\n  width: 100%;\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space_1.default(1), function (p) { return p.theme.fontSizeMedium; });
var AuthorName = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis_1.default);
var Commits = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  text-align: right;\n"], ["\n  color: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.subText; });
var Percent = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  min-width: 40px;\n  text-align: right;\n"], ["\n  min-width: 40px;\n  text-align: right;\n"])));
exports.default = CommitAuthorBreakdown;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=commitAuthorBreakdown.jsx.map