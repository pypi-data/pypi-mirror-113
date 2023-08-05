Object.defineProperty(exports, "__esModule", { value: true });
exports.DownloadStatus = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dataExport_1 = require("app/components/dataExport");
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var layout_1 = tslib_1.__importDefault(require("app/views/auth/layout"));
var DownloadStatus;
(function (DownloadStatus) {
    DownloadStatus["Early"] = "EARLY";
    DownloadStatus["Valid"] = "VALID";
    DownloadStatus["Expired"] = "EXPIRED";
})(DownloadStatus = exports.DownloadStatus || (exports.DownloadStatus = {}));
var DataDownload = /** @class */ (function (_super) {
    tslib_1.__extends(DataDownload, _super);
    function DataDownload() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DataDownload.prototype.getTitle = function () {
        return locale_1.t('Download Center');
    };
    DataDownload.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, dataExportId = _a.dataExportId;
        return [['download', "/organizations/" + orgId + "/data-export/" + dataExportId + "/"]];
    };
    DataDownload.prototype.getActionLink = function (queryType) {
        var orgId = this.props.params.orgId;
        switch (queryType) {
            case dataExport_1.ExportQueryType.IssuesByTag:
                return "/organizations/" + orgId + "/issues/";
            case dataExport_1.ExportQueryType.Discover:
                return "/organizations/" + orgId + "/discover/queries/";
            default:
                return '/';
        }
    };
    DataDownload.prototype.renderDate = function (date) {
        if (!date) {
            return null;
        }
        var d = new Date(date);
        return (<strong>
        <dateTime_1.default date={d}/>
      </strong>);
    };
    DataDownload.prototype.renderEarly = function () {
        return (<React.Fragment>
        <Header>
          <h3>
            {locale_1.t('What are')}
            <i>{locale_1.t(' you ')}</i>
            {locale_1.t('doing here?')}
          </h3>
        </Header>
        <Body>
          <p>
            {locale_1.t("Not that its any of our business, but were you invited to this page? It's just that we don't exactly remember emailing you about it.")}
          </p>
          <p>{locale_1.t("Close this window and we'll email you when your download is ready.")}</p>
        </Body>
      </React.Fragment>);
    };
    DataDownload.prototype.renderExpired = function () {
        var query = this.state.download.query;
        var actionLink = this.getActionLink(query.type);
        return (<React.Fragment>
        <Header>
          <h3>{locale_1.t('This is awkward.')}</h3>
        </Header>
        <Body>
          <p>
            {locale_1.t("That link expired, so your download doesn't live here anymore. Just picked up one day and left town.")}
          </p>
          <p>
            {locale_1.t('Make a new one with your latest data. Your old download will never see it coming.')}
          </p>
          <DownloadButton href={actionLink} priority="primary">
            {locale_1.t('Start a New Download')}
          </DownloadButton>
        </Body>
      </React.Fragment>);
    };
    DataDownload.prototype.openInDiscover = function () {
        var info = this.state.download.query.info;
        var orgId = this.props.params.orgId;
        var to = {
            pathname: "/organizations/" + orgId + "/discover/results/",
            query: info,
        };
        react_router_1.browserHistory.push(to);
    };
    DataDownload.prototype.renderOpenInDiscover = function () {
        var _this = this;
        var _a = this.state.download.query, query = _a === void 0 ? {
            type: dataExport_1.ExportQueryType.IssuesByTag,
            info: {},
        } : _a;
        // default to IssuesByTag because we dont want to
        // display this unless we're sure its a discover query
        var _b = query.type, type = _b === void 0 ? dataExport_1.ExportQueryType.IssuesByTag : _b;
        return type === 'Discover' ? (<React.Fragment>
        <p>{locale_1.t('Need to make changes?')}</p>
        <button_1.default priority="primary" onClick={function () { return _this.openInDiscover(); }}>
          {locale_1.t('Open in Discover')}
        </button_1.default>
        <br />
      </React.Fragment>) : null;
    };
    DataDownload.prototype.renderValid = function () {
        var _a = this.state.download, dateExpired = _a.dateExpired, checksum = _a.checksum;
        var _b = this.props.params, orgId = _b.orgId, dataExportId = _b.dataExportId;
        return (<React.Fragment>
        <Header>
          <h3>{locale_1.t('All done.')}</h3>
        </Header>
        <Body>
          <p>{locale_1.t("See, that wasn't so bad. Your data is all ready for download.")}</p>
          <button_1.default priority="primary" icon={<icons_1.IconDownload />} href={"/api/0/organizations/" + orgId + "/data-export/" + dataExportId + "/?download=true"}>
            {locale_1.t('Download CSV')}
          </button_1.default>
          <p>
            {locale_1.t("That link won't last forever — it expires:")}
            <br />
            {this.renderDate(dateExpired)}
          </p>
          {this.renderOpenInDiscover()}
          <p>
            <small>
              <strong>SHA1:{checksum}</strong>
            </small>
            <br />
            {locale_1.tct('Need help verifying? [link].', {
                link: (<a href="https://docs.sentry.io/product/discover-queries/query-builder/#filter-by-table-columns" target="_blank" rel="noopener noreferrer">
                  {locale_1.t('Check out our docs')}
                </a>),
            })}
          </p>
        </Body>
      </React.Fragment>);
    };
    DataDownload.prototype.renderError = function () {
        var _a;
        var err = this.state.errors.download;
        var errDetail = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail;
        return (<layout_1.default>
        <main>
          <Header>
            <h3>
              {err.status} - {err.statusText}
            </h3>
          </Header>
          {errDetail && (<Body>
              <p>{errDetail}</p>
            </Body>)}
        </main>
      </layout_1.default>);
    };
    DataDownload.prototype.renderContent = function () {
        var download = this.state.download;
        switch (download.status) {
            case DownloadStatus.Early:
                return this.renderEarly();
            case DownloadStatus.Expired:
                return this.renderExpired();
            default:
                return this.renderValid();
        }
    };
    DataDownload.prototype.renderBody = function () {
        return (<layout_1.default>
        <main>{this.renderContent()}</main>
      </layout_1.default>);
    };
    return DataDownload;
}(asyncView_1.default));
var Header = styled_1.default('header')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  padding: ", " 40px 0;\n  h3 {\n    font-size: 24px;\n    margin: 0 0 ", " 0;\n  }\n"], ["\n  border-bottom: 1px solid ", ";\n  padding: ", " 40px 0;\n  h3 {\n    font-size: 24px;\n    margin: 0 0 ", " 0;\n  }\n"])), function (p) { return p.theme.border; }, space_1.default(3), space_1.default(3));
var Body = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding: ", " 40px;\n  max-width: 500px;\n  p {\n    margin: ", " 0;\n  }\n"], ["\n  padding: ", " 40px;\n  max-width: 500px;\n  p {\n    margin: ", " 0;\n  }\n"])), space_1.default(2), space_1.default(1.5));
var DownloadButton = styled_1.default(button_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
exports.default = DataDownload;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=dataDownload.jsx.map