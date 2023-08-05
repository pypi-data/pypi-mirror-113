Object.defineProperty(exports, "__esModule", { value: true });
exports.Line = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var classnames_1 = tslib_1.__importDefault(require("classnames"));
var scroll_to_element_1 = tslib_1.__importDefault(require("scroll-to-element"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var utils_1 = require("app/components/events/interfaces/debugMeta/utils");
var packageLink_1 = tslib_1.__importDefault(require("app/components/events/interfaces/packageLink"));
var packageStatus_1 = tslib_1.__importStar(require("app/components/events/interfaces/packageStatus"));
var togglableAddress_1 = tslib_1.__importStar(require("app/components/events/interfaces/togglableAddress"));
var types_1 = require("app/components/events/interfaces/types");
var stacktracePreview_1 = require("app/components/stacktracePreview");
var strictClick_1 = tslib_1.__importDefault(require("app/components/strictClick"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var debugMetaStore_1 = require("app/stores/debugMetaStore");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withSentryAppComponents_1 = tslib_1.__importDefault(require("app/utils/withSentryAppComponents"));
var context_1 = tslib_1.__importDefault(require("./context"));
var defaultTitle_1 = tslib_1.__importDefault(require("./defaultTitle"));
var symbol_1 = tslib_1.__importStar(require("./symbol"));
var utils_3 = require("./utils");
function makeFilter(addr, addrMode, image) {
    if (!(!addrMode || addrMode === 'abs') && image) {
        return image.debug_id + "!" + addr;
    }
    return addr;
}
var Line = /** @class */ (function (_super) {
    tslib_1.__extends(Line, _super);
    function Line() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // isExpanded can be initialized to true via parent component;
        // data synchronization is not important
        // https://facebook.github.io/react/tips/props-in-getInitialState-as-anti-pattern.html
        _this.state = {
            isExpanded: _this.props.isExpanded,
        };
        _this.toggleContext = function (evt) {
            evt && evt.preventDefault();
            _this.setState({
                isExpanded: !_this.state.isExpanded,
            });
        };
        _this.scrollToImage = function (event) {
            event.stopPropagation(); // to prevent collapsing if collapsable
            var _a = _this.props.data, instructionAddr = _a.instructionAddr, addrMode = _a.addrMode;
            if (instructionAddr) {
                debugMetaStore_1.DebugMetaActions.updateFilter(makeFilter(instructionAddr, addrMode, _this.props.image));
            }
            scroll_to_element_1.default('#images-loaded');
        };
        _this.preventCollapse = function (evt) {
            evt.stopPropagation();
        };
        return _this;
    }
    Line.prototype.hasContextSource = function () {
        return utils_2.defined(this.props.data.context) && !!this.props.data.context.length;
    };
    Line.prototype.hasContextVars = function () {
        return !utils_2.objectIsEmpty(this.props.data.vars || {});
    };
    Line.prototype.hasContextRegisters = function () {
        return !utils_2.objectIsEmpty(this.props.registers);
    };
    Line.prototype.hasAssembly = function () {
        return utils_3.isDotnet(this.getPlatform()) && utils_2.defined(this.props.data.package);
    };
    Line.prototype.isExpandable = function () {
        return ((!this.props.isOnlyFrame && this.props.emptySourceNotation) ||
            this.hasContextSource() ||
            this.hasContextVars() ||
            this.hasContextRegisters() ||
            this.hasAssembly());
    };
    Line.prototype.getPlatform = function () {
        var _a;
        // prioritize the frame platform but fall back to the platform
        // of the stack trace / exception
        return utils_3.getPlatform(this.props.data.platform, (_a = this.props.platform) !== null && _a !== void 0 ? _a : 'other');
    };
    Line.prototype.isInlineFrame = function () {
        return (this.props.prevFrame &&
            this.getPlatform() === (this.props.prevFrame.platform || this.props.platform) &&
            this.props.data.instructionAddr === this.props.prevFrame.instructionAddr);
    };
    Line.prototype.shouldShowLinkToImage = function () {
        var _a = this.props, isHoverPreviewed = _a.isHoverPreviewed, data = _a.data;
        var symbolicatorStatus = data.symbolicatorStatus;
        return (!!symbolicatorStatus &&
            symbolicatorStatus !== types_1.SymbolicatorStatus.UNKNOWN_IMAGE &&
            !isHoverPreviewed);
    };
    Line.prototype.packageStatus = function () {
        // this is the status of image that belongs to this frame
        var image = this.props.image;
        if (!image) {
            return 'empty';
        }
        var combinedStatus = utils_1.combineStatus(image.debug_status, image.unwind_status);
        switch (combinedStatus) {
            case 'unused':
                return 'empty';
            case 'found':
                return 'success';
            default:
                return 'error';
        }
    };
    Line.prototype.renderExpander = function () {
        if (!this.isExpandable()) {
            return null;
        }
        var isHoverPreviewed = this.props.isHoverPreviewed;
        var isExpanded = this.state.isExpanded;
        return (<ToggleContextButtonWrapper>
        <ToggleContextButton className="btn-toggle" css={utils_3.isDotnet(this.getPlatform()) && { display: 'block !important' }} // remove important once we get rid of css files
         title={locale_1.t('Toggle Context')} tooltipProps={isHoverPreviewed ? { delay: stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY } : undefined} onClick={this.toggleContext}>
          <icons_1.IconChevron direction={isExpanded ? 'up' : 'down'} size="8px"/>
        </ToggleContextButton>
      </ToggleContextButtonWrapper>);
    };
    Line.prototype.leadsToApp = function () {
        var _a = this.props, data = _a.data, nextFrame = _a.nextFrame;
        return !data.inApp && ((nextFrame && nextFrame.inApp) || !nextFrame);
    };
    Line.prototype.isFoundByStackScanning = function () {
        var data = this.props.data;
        return data.trust === 'scan' || data.trust === 'cfi-scan';
    };
    Line.prototype.renderLeadHint = function () {
        var isExpanded = this.state.isExpanded;
        if (isExpanded) {
            return null;
        }
        var leadsToApp = this.leadsToApp();
        if (!leadsToApp) {
            return null;
        }
        var nextFrame = this.props.nextFrame;
        return !nextFrame ? (<LeadHint className="leads-to-app-hint" width="115px">
        {locale_1.t('Crashed in non-app')}
        {': '}
      </LeadHint>) : (<LeadHint className="leads-to-app-hint">
        {locale_1.t('Called from')}
        {': '}
      </LeadHint>);
    };
    Line.prototype.renderRepeats = function () {
        var timesRepeated = this.props.timesRepeated;
        if (timesRepeated && timesRepeated > 0) {
            return (<RepeatedFrames title={"Frame repeated " + timesRepeated + " time" + (timesRepeated === 1 ? '' : 's')}>
          <RepeatedContent>
            <StyledIconRefresh />
            <span>{timesRepeated}</span>
          </RepeatedContent>
        </RepeatedFrames>);
        }
        return null;
    };
    Line.prototype.renderDefaultLine = function () {
        var _a;
        var isHoverPreviewed = this.props.isHoverPreviewed;
        return (<strictClick_1.default onClick={this.isExpandable() ? this.toggleContext : undefined}>
        <DefaultLine className="title">
          <VertCenterWrapper>
            <div>
              {this.renderLeadHint()}
              <defaultTitle_1.default frame={this.props.data} platform={(_a = this.props.platform) !== null && _a !== void 0 ? _a : 'other'} isHoverPreviewed={isHoverPreviewed}/>
            </div>
            {this.renderRepeats()}
          </VertCenterWrapper>
          {this.renderExpander()}
        </DefaultLine>
      </strictClick_1.default>);
    };
    Line.prototype.renderNativeLine = function () {
        var _a = this.props, data = _a.data, showingAbsoluteAddress = _a.showingAbsoluteAddress, onAddressToggle = _a.onAddressToggle, onFunctionNameToggle = _a.onFunctionNameToggle, image = _a.image, maxLengthOfRelativeAddress = _a.maxLengthOfRelativeAddress, includeSystemFrames = _a.includeSystemFrames, isFrameAfterLastNonApp = _a.isFrameAfterLastNonApp, showCompleteFunctionName = _a.showCompleteFunctionName, isHoverPreviewed = _a.isHoverPreviewed;
        var leadHint = this.renderLeadHint();
        var packageStatus = this.packageStatus();
        return (<strictClick_1.default onClick={this.isExpandable() ? this.toggleContext : undefined}>
        <DefaultLine className="title as-table">
          <NativeLineContent isFrameAfterLastNonApp={!!isFrameAfterLastNonApp}>
            <PackageInfo>
              {leadHint}
              <packageLink_1.default includeSystemFrames={!!includeSystemFrames} withLeadHint={leadHint !== null} packagePath={data.package} onClick={this.scrollToImage} isClickable={this.shouldShowLinkToImage()} isHoverPreviewed={isHoverPreviewed}>
                {!isHoverPreviewed && (<packageStatus_1.default status={packageStatus} tooltip={locale_1.t('Go to Images Loaded')}/>)}
              </packageLink_1.default>
            </PackageInfo>
            {data.instructionAddr && (<togglableAddress_1.default address={data.instructionAddr} startingAddress={image ? image.image_addr : null} isAbsolute={!!showingAbsoluteAddress} isFoundByStackScanning={this.isFoundByStackScanning()} isInlineFrame={!!this.isInlineFrame()} onToggle={onAddressToggle} relativeAddressMaxlength={maxLengthOfRelativeAddress} isHoverPreviewed={isHoverPreviewed}/>)}
            <symbol_1.default frame={data} showCompleteFunctionName={!!showCompleteFunctionName} onFunctionNameToggle={onFunctionNameToggle} isHoverPreviewed={isHoverPreviewed}/>
          </NativeLineContent>
          {this.renderExpander()}
        </DefaultLine>
      </strictClick_1.default>);
    };
    Line.prototype.renderLine = function () {
        switch (this.getPlatform()) {
            case 'objc':
            // fallthrough
            case 'cocoa':
            // fallthrough
            case 'native':
                return this.renderNativeLine();
            default:
                return this.renderDefaultLine();
        }
    };
    Line.prototype.render = function () {
        var data = this.props.data;
        var className = classnames_1.default({
            frame: true,
            'is-expandable': this.isExpandable(),
            expanded: this.state.isExpanded,
            collapsed: !this.state.isExpanded,
            'system-frame': !data.inApp,
            'frame-errors': data.errors,
            'leads-to-app': this.leadsToApp(),
        });
        var props = { className: className };
        return (<StyledLi {...props}>
        {this.renderLine()}
        <context_1.default frame={data} event={this.props.event} registers={this.props.registers} components={this.props.components} hasContextSource={this.hasContextSource()} hasContextVars={this.hasContextVars()} hasContextRegisters={this.hasContextRegisters()} emptySourceNotation={this.props.emptySourceNotation} hasAssembly={this.hasAssembly()} expandable={this.isExpandable()} isExpanded={this.state.isExpanded}/>
      </StyledLi>);
    };
    Line.defaultProps = {
        isExpanded: false,
        emptySourceNotation: false,
        isHoverPreviewed: false,
    };
    return Line;
}(React.Component));
exports.Line = Line;
exports.default = withOrganization_1.default(withSentryAppComponents_1.default(Line, { componentType: 'stacktrace-link' }));
var RepeatedFrames = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  border-radius: 50px;\n  padding: 1px 3px;\n  margin-left: ", ";\n  border-width: thin;\n  border-style: solid;\n  border-color: ", ";\n  color: ", ";\n  background-color: ", ";\n  white-space: nowrap;\n"], ["\n  display: inline-block;\n  border-radius: 50px;\n  padding: 1px 3px;\n  margin-left: ", ";\n  border-width: thin;\n  border-style: solid;\n  border-color: ", ";\n  color: ", ";\n  background-color: ", ";\n  white-space: nowrap;\n"])), space_1.default(1), function (p) { return p.theme.orange500; }, function (p) { return p.theme.orange500; }, function (p) { return p.theme.backgroundSecondary; });
var VertCenterWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var RepeatedContent = styled_1.default(VertCenterWrapper)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  justify-content: center;\n"], ["\n  justify-content: center;\n"])));
var PackageInfo = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  order: 2;\n  align-items: flex-start;\n  @media (min-width: ", ") {\n    order: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  order: 2;\n  align-items: flex-start;\n  @media (min-width: ", ") {\n    order: 0;\n  }\n"])), function (props) { return props.theme.breakpoints[0]; });
var NativeLineContent = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  flex: 1;\n  grid-gap: ", ";\n  grid-template-columns: ", ";\n  align-items: center;\n  justify-content: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n"], ["\n  display: grid;\n  flex: 1;\n  grid-gap: ", ";\n  grid-template-columns: ", ";\n  align-items: center;\n  justify-content: flex-start;\n\n  @media (min-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns:\n      ", " minmax(117px, auto)\n      1fr;\n  }\n"])), space_1.default(0.5), function (p) {
    return "minmax(" + (p.isFrameAfterLastNonApp ? '167px' : '117px') + ", auto)  1fr";
}, function (props) { return props.theme.breakpoints[0]; }, function (p) { return (p.isFrameAfterLastNonApp ? '200px' : '150px'); }, function (props) { return props.theme.breakpoints[2]; }, function (props) {
    return props.theme.breakpoints[3];
}, function (p) { return (p.isFrameAfterLastNonApp ? '180px' : '140px'); });
var DefaultLine = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr auto;\n  align-items: center;\n"])));
var StyledIconRefresh = styled_1.default(icons_1.IconRefresh)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.25));
var LeadHint = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  ", "\n  max-width: ", "\n"], ["\n  ", "\n  max-width: ", "\n"])), overflowEllipsis_1.default, function (p) { return (p.width ? p.width : '67px'); });
var ToggleContextButtonWrapper = styled_1.default('span')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space_1.default(1));
// the Button's label has the padding of 3px because the button size has to be 16x16 px.
var ToggleContextButton = styled_1.default(button_1.default)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  span:first-child {\n    padding: 3px;\n  }\n"], ["\n  span:first-child {\n    padding: 3px;\n  }\n"])));
var StyledLi = styled_1.default('li')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  ", " {\n    flex-shrink: 0;\n  }\n  :hover {\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n  }\n"], ["\n  ", " {\n    flex-shrink: 0;\n  }\n  :hover {\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n    ", " {\n      visibility: visible;\n    }\n  }\n"])), packageStatus_1.PackageStatusIcon, packageStatus_1.PackageStatusIcon, togglableAddress_1.AddressToggleIcon, symbol_1.FunctionNameToggleIcon);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=line.jsx.map