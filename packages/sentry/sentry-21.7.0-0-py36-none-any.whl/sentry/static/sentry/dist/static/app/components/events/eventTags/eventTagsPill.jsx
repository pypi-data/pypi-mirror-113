Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var react_1 = require("@emotion/react");
var queryString = tslib_1.__importStar(require("query-string"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pill_1 = tslib_1.__importDefault(require("app/components/pill"));
var versionHoverCard_1 = tslib_1.__importDefault(require("app/components/versionHoverCard"));
var icons_1 = require("app/icons");
var utils_1 = require("app/utils");
var eventTagsPillValue_1 = tslib_1.__importDefault(require("./eventTagsPillValue"));
var iconStyle = react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var EventTagsPill = function (_a) {
    var tag = _a.tag, query = _a.query, organization = _a.organization, projectId = _a.projectId, streamPath = _a.streamPath, releasesPath = _a.releasesPath;
    var locationSearch = "?" + queryString.stringify(query);
    var key = tag.key, value = tag.value;
    var isRelease = key === 'release';
    var name = !key ? <annotatedText_1.default value={key} meta={metaProxy_1.getMeta(tag, 'key')}/> : key;
    var type = !key ? 'error' : undefined;
    return (<pill_1.default name={name} value={value} type={type}>
      <eventTagsPillValue_1.default tag={tag} meta={metaProxy_1.getMeta(tag, 'value')} streamPath={streamPath} locationSearch={locationSearch} isRelease={isRelease}/>
      {utils_1.isUrl(value) && (<externalLink_1.default href={value} className="external-icon">
          <icons_1.IconOpen size="xs" css={iconStyle}/>
        </externalLink_1.default>)}
      {isRelease && (<div className="pill-icon">
          <versionHoverCard_1.default organization={organization} projectSlug={projectId} releaseVersion={value}>
            <react_router_1.Link to={{ pathname: "" + releasesPath + value + "/", search: locationSearch }}>
              <icons_1.IconInfo size="xs" css={iconStyle}/>
            </react_router_1.Link>
          </versionHoverCard_1.default>
        </div>)}
    </pill_1.default>);
};
exports.default = EventTagsPill;
var templateObject_1;
//# sourceMappingURL=eventTagsPill.jsx.map