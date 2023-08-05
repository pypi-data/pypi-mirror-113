Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var annotatedText_1 = tslib_1.__importDefault(require("app/components/events/meta/annotatedText"));
var metaProxy_1 = require("app/components/events/meta/metaProxy");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var stacktracePreview_1 = require("app/components/stacktracePreview");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var truncate_1 = tslib_1.__importDefault(require("app/components/truncate"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var functionName_1 = tslib_1.__importDefault(require("../functionName"));
var utils_2 = require("../utils");
var originalSourceInfo_1 = tslib_1.__importDefault(require("./originalSourceInfo"));
var DefaultTitle = function (_a) {
    var frame = _a.frame, platform = _a.platform, isHoverPreviewed = _a.isHoverPreviewed;
    var title = [];
    var framePlatform = utils_2.getPlatform(frame.platform, platform);
    var tooltipDelay = isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined;
    var handleExternalLink = function (event) {
        event.stopPropagation();
    };
    var getModule = function () {
        if (frame.module) {
            return {
                key: 'module',
                value: frame.module,
                meta: metaProxy_1.getMeta(frame, 'module'),
            };
        }
        return undefined;
    };
    var getPathNameOrModule = function (shouldPrioritizeModuleName) {
        if (shouldPrioritizeModuleName) {
            if (frame.module) {
                return getModule();
            }
            if (frame.filename) {
                return {
                    key: 'filename',
                    value: frame.filename,
                    meta: metaProxy_1.getMeta(frame, 'filename'),
                };
            }
            return undefined;
        }
        if (frame.filename) {
            return {
                key: 'filename',
                value: frame.filename,
                meta: metaProxy_1.getMeta(frame, 'filename'),
            };
        }
        if (frame.module) {
            return getModule();
        }
        return undefined;
    };
    // TODO(dcramer): this needs to use a formatted string so it can be
    // localized correctly
    if (utils_1.defined(frame.filename || frame.module)) {
        // prioritize module name for Java as filename is often only basename
        var shouldPrioritizeModuleName = framePlatform === 'java';
        // we do not want to show path in title on csharp platform
        var pathNameOrModule = utils_2.isDotnet(framePlatform)
            ? getModule()
            : getPathNameOrModule(shouldPrioritizeModuleName);
        var enablePathTooltip = utils_1.defined(frame.absPath) && frame.absPath !== (pathNameOrModule === null || pathNameOrModule === void 0 ? void 0 : pathNameOrModule.value);
        if (pathNameOrModule) {
            title.push(<tooltip_1.default key={pathNameOrModule.key} title={frame.absPath} disabled={!enablePathTooltip} delay={tooltipDelay}>
          <code key="filename" className="filename">
            <annotatedText_1.default value={<truncate_1.default value={pathNameOrModule.value} maxLength={100} leftTrim/>} meta={pathNameOrModule.meta}/>
          </code>
        </tooltip_1.default>);
        }
        // in case we prioritized the module name but we also have a filename info
        // we want to show a litle (?) icon that on hover shows the actual filename
        if (shouldPrioritizeModuleName && frame.filename) {
            title.push(<tooltip_1.default key={frame.filename} title={frame.filename} delay={tooltipDelay}>
          <a className="in-at real-filename">
            <icons_1.IconQuestion size="xs"/>
          </a>
        </tooltip_1.default>);
        }
        if (frame.absPath && utils_1.isUrl(frame.absPath)) {
            title.push(<StyledExternalLink href={frame.absPath} key="share" onClick={handleExternalLink}>
          <icons_1.IconOpen size="xs"/>
        </StyledExternalLink>);
        }
        if ((utils_1.defined(frame.function) || utils_1.defined(frame.rawFunction)) &&
            utils_1.defined(pathNameOrModule)) {
            title.push(<InFramePosition className="in-at" key="in">
          {" " + locale_1.t('in') + " "}
        </InFramePosition>);
        }
    }
    if (utils_1.defined(frame.function) || utils_1.defined(frame.rawFunction)) {
        title.push(<functionName_1.default frame={frame} key="function" className="function"/>);
    }
    // we don't want to render out zero line numbers which are used to
    // indicate lack of source information for native setups.  We could
    // TODO(mitsuhiko): only do this for events from native platforms?
    if (utils_1.defined(frame.lineNo) && frame.lineNo !== 0) {
        title.push(<InFramePosition className="in-at in-at-line" key="no">
        {" " + locale_1.t('at line') + " "}
      </InFramePosition>);
        title.push(<code key="line" className="lineno">
        {utils_1.defined(frame.colNo) ? frame.lineNo + ":" + frame.colNo : frame.lineNo}
      </code>);
    }
    if (utils_1.defined(frame.package) && !utils_2.isDotnet(framePlatform)) {
        title.push(<InFramePosition key="within">{" " + locale_1.t('within') + " "}</InFramePosition>);
        title.push(<code title={frame.package} className="package" key="package">
        {utils_2.trimPackage(frame.package)}
      </code>);
    }
    if (utils_1.defined(frame.origAbsPath)) {
        title.push(<tooltip_1.default key="info-tooltip" title={<originalSourceInfo_1.default mapUrl={frame.mapUrl} map={frame.map}/>} delay={tooltipDelay}>
        <a className="in-at original-src">
          <icons_1.IconQuestion size="xs"/>
        </a>
      </tooltip_1.default>);
    }
    return <React.Fragment>{title}</React.Fragment>;
};
exports.default = DefaultTitle;
var StyledExternalLink = styled_1.default(externalLink_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  top: ", ";\n  margin-left: ", ";\n"], ["\n  position: relative;\n  top: ", ";\n  margin-left: ", ";\n"])), space_1.default(0.25), space_1.default(0.5));
var InFramePosition = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  opacity: 0.6;\n"], ["\n  color: ", ";\n  opacity: 0.6;\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map