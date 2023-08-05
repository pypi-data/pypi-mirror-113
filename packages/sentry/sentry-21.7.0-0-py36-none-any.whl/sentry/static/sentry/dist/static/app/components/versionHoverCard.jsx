Object.defineProperty(exports, "__esModule", { value: true });
exports.VersionHoverCard = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var avatarList_1 = tslib_1.__importDefault(require("app/components/avatar/avatarList"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var clipboard_1 = tslib_1.__importDefault(require("app/components/clipboard"));
var hovercard_1 = tslib_1.__importDefault(require("app/components/hovercard"));
var lastCommit_1 = tslib_1.__importDefault(require("app/components/lastCommit"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var repoLabel_1 = tslib_1.__importDefault(require("app/components/repoLabel"));
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withRelease_1 = tslib_1.__importDefault(require("app/utils/withRelease"));
var withRepositories_1 = tslib_1.__importDefault(require("app/utils/withRepositories"));
var VersionHoverCard = /** @class */ (function (_super) {
    tslib_1.__extends(VersionHoverCard, _super);
    function VersionHoverCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            visible: false,
        };
        return _this;
    }
    VersionHoverCard.prototype.toggleHovercard = function () {
        this.setState({
            visible: true,
        });
    };
    VersionHoverCard.prototype.getRepoLink = function () {
        var organization = this.props.organization;
        var orgSlug = organization.slug;
        return {
            header: null,
            body: (<ConnectRepo>
          <h5>{locale_1.t('Releases are better with commit data!')}</h5>
          <p>
            {locale_1.t('Connect a repository to see commit info, files changed, and authors involved in future releases.')}
          </p>
          <button_1.default href={"/organizations/" + orgSlug + "/repos/"} priority="primary">
            {locale_1.t('Connect a repository')}
          </button_1.default>
        </ConnectRepo>),
        };
    };
    VersionHoverCard.prototype.getBody = function () {
        var _a = this.props, releaseVersion = _a.releaseVersion, release = _a.release, deploys = _a.deploys;
        if (release === undefined || !utils_1.defined(deploys)) {
            return { header: null, body: null };
        }
        var lastCommit = release.lastCommit;
        var recentDeploysByEnvironment = deploys.reduce(function (dbe, deploy) {
            var dateFinished = deploy.dateFinished, environment = deploy.environment;
            if (!dbe.hasOwnProperty(environment)) {
                dbe[environment] = dateFinished;
            }
            return dbe;
        }, {});
        var mostRecentDeploySlice = Object.keys(recentDeploysByEnvironment);
        if (Object.keys(recentDeploysByEnvironment).length > 3) {
            mostRecentDeploySlice = Object.keys(recentDeploysByEnvironment).slice(0, 3);
        }
        return {
            header: (<HeaderWrapper>
          {locale_1.t('Release')}
          <VersionWrapper>
            <StyledVersion version={releaseVersion} truncate anchor={false}/>

            <clipboard_1.default value={releaseVersion}>
              <ClipboardIconWrapper>
                <icons_1.IconCopy size="xs"/>
              </ClipboardIconWrapper>
            </clipboard_1.default>
          </VersionWrapper>
        </HeaderWrapper>),
            body: (<div>
          <div className="row row-flex">
            <div className="col-xs-4">
              <h6>{locale_1.t('New Issues')}</h6>
              <div className="count-since">{release.newGroups}</div>
            </div>
            <div className="col-xs-8">
              <h6 style={{ textAlign: 'right' }}>
                {release.commitCount}{' '}
                {release.commitCount !== 1 ? locale_1.t('commits ') : locale_1.t('commit ')} {locale_1.t('by ')}{' '}
                {release.authors.length}{' '}
                {release.authors.length !== 1 ? locale_1.t('authors') : locale_1.t('author')}{' '}
              </h6>
              <avatarList_1.default users={release.authors} avatarSize={25} tooltipOptions={{ container: 'body' }} typeMembers="authors"/>
            </div>
          </div>
          {lastCommit && <lastCommit_1.default commit={lastCommit} headerClass="commit-heading"/>}
          {deploys.length > 0 && (<div>
              <div className="divider">
                <h6 className="deploy-heading">{locale_1.t('Deploys')}</h6>
              </div>
              {mostRecentDeploySlice.map(function (env, idx) {
                        var dateFinished = recentDeploysByEnvironment[env];
                        return (<div className="deploy" key={idx}>
                    <div className="deploy-meta" style={{ position: 'relative' }}>
                      <VersionRepoLabel>{env}</VersionRepoLabel>
                      {dateFinished && <StyledTimeSince date={dateFinished}/>}
                    </div>
                  </div>);
                    })}
            </div>)}
        </div>),
        };
    };
    VersionHoverCard.prototype.render = function () {
        var _a;
        var _b = this.props, deploysLoading = _b.deploysLoading, deploysError = _b.deploysError, release = _b.release, releaseLoading = _b.releaseLoading, releaseError = _b.releaseError, repositories = _b.repositories, repositoriesLoading = _b.repositoriesLoading, repositoriesError = _b.repositoriesError;
        var header = null;
        var body = null;
        var loading = !!(deploysLoading || releaseLoading || repositoriesLoading);
        var error = (_a = deploysError !== null && deploysError !== void 0 ? deploysError : releaseError) !== null && _a !== void 0 ? _a : repositoriesError;
        var hasRepos = repositories && repositories.length > 0;
        if (loading) {
            body = <loadingIndicator_1.default mini/>;
        }
        else if (error) {
            body = <loadingError_1.default />;
        }
        else {
            var renderObj = hasRepos && release ? this.getBody() : this.getRepoLink();
            header = renderObj.header;
            body = renderObj.body;
        }
        return (<hovercard_1.default {...this.props} header={header} body={body}>
        {this.props.children}
      </hovercard_1.default>);
    };
    return VersionHoverCard;
}(React.Component));
exports.VersionHoverCard = VersionHoverCard;
exports.default = withApi_1.default(withRelease_1.default(withRepositories_1.default(VersionHoverCard)));
var ConnectRepo = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  text-align: center;\n"], ["\n  padding: ", ";\n  text-align: center;\n"])), space_1.default(2));
var VersionRepoLabel = styled_1.default(repoLabel_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 86px;\n"], ["\n  width: 86px;\n"])));
var StyledTimeSince = styled_1.default(timeSince_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  position: absolute;\n  left: 98px;\n  width: 50%;\n  padding: 3px 0;\n"], ["\n  color: ", ";\n  position: absolute;\n  left: 98px;\n  width: 50%;\n  padding: 3px 0;\n"])), function (p) { return p.theme.gray300; });
var HeaderWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n"])));
var VersionWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  flex: 1;\n  align-items: center;\n  justify-content: flex-end;\n"])));
var StyledVersion = styled_1.default(version_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  max-width: 190px;\n"], ["\n  margin-right: ", ";\n  max-width: 190px;\n"])), space_1.default(0.5));
var ClipboardIconWrapper = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  &:hover {\n    cursor: pointer;\n  }\n"], ["\n  &:hover {\n    cursor: pointer;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=versionHoverCard.jsx.map