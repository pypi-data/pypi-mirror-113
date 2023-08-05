Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isNil_1 = tslib_1.__importDefault(require("lodash/isNil"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var debugFileFeature_1 = tslib_1.__importDefault(require("app/components/debugFileFeature"));
var utils_1 = require("app/components/events/interfaces/utils");
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("./utils");
var IMAGE_ADDR_LEN = 12;
function getImageStatusText(status) {
    switch (status) {
        case 'found':
            return locale_1.t('ok');
        case 'unused':
            return locale_1.t('unused');
        case 'missing':
            return locale_1.t('missing');
        case 'malformed':
        case 'fetching_failed':
        case 'timeout':
        case 'other':
            return locale_1.t('failed');
        default:
            return null;
    }
}
function getImageStatusDetails(status) {
    switch (status) {
        case 'found':
            return locale_1.t('Debug information for this image was found and successfully processed.');
        case 'unused':
            return locale_1.t('The image was not required for processing the stack trace.');
        case 'missing':
            return locale_1.t('No debug information could be found in any of the specified sources.');
        case 'malformed':
            return locale_1.t('The debug information file for this image failed to process.');
        case 'timeout':
        case 'fetching_failed':
            return locale_1.t('The debug information file for this image could not be downloaded.');
        case 'other':
            return locale_1.t('An internal error occurred while handling this image.');
        default:
            return null;
    }
}
var DebugImage = React.memo(function (_a) {
    var image = _a.image, organization = _a.organization, projectId = _a.projectId, showDetails = _a.showDetails, style = _a.style;
    var orgSlug = organization.slug;
    var getSettingsLink = function () {
        if (!orgSlug || !projectId || !image.debug_id) {
            return null;
        }
        return "/settings/" + orgSlug + "/projects/" + projectId + "/debug-symbols/?query=" + image.debug_id;
    };
    var renderStatus = function (title, status) {
        if (isNil_1.default(status)) {
            return null;
        }
        var text = getImageStatusText(status);
        if (!text) {
            return null;
        }
        return (<SymbolicationStatus>
          <tooltip_1.default title={getImageStatusDetails(status)}>
            <span>
              <ImageProp>{title}</ImageProp>: {text}
            </span>
          </tooltip_1.default>
        </SymbolicationStatus>);
    };
    var combinedStatus = utils_2.combineStatus(image.debug_status, image.unwind_status);
    var _b = tslib_1.__read(utils_1.getImageRange(image), 2), startAddress = _b[0], endAddress = _b[1];
    var renderIconElement = function () {
        switch (combinedStatus) {
            case 'unused':
                return (<IconWrapper>
              <icons_1.IconCircle />
            </IconWrapper>);
            case 'found':
                return (<IconWrapper>
              <icons_1.IconCheckmark isCircled color="green300"/>
            </IconWrapper>);
            default:
                return (<IconWrapper>
              <icons_1.IconFlag color="red300"/>
            </IconWrapper>);
        }
    };
    var codeFile = utils_2.getFileName(image.code_file);
    var debugFile = image.debug_file && utils_2.getFileName(image.debug_file);
    // The debug file is only realistically set on Windows. All other platforms
    // either leave it empty or set it to a filename thats equal to the code
    // file name. In this case, do not show it.
    var showDebugFile = debugFile && codeFile !== debugFile;
    // Availability only makes sense if the image is actually referenced.
    // Otherwise, the processing pipeline does not resolve this kind of
    // information and it will always be false.
    var showAvailability = !isNil_1.default(image.features) && combinedStatus !== 'unused';
    // The code id is sometimes missing, and sometimes set to the equivalent of
    // the debug id (e.g. for Mach symbols). In this case, it is redundant
    // information and we do not want to show it.
    var showCodeId = !!image.code_id && image.code_id !== image.debug_id;
    // Old versions of the event pipeline did not store the symbolication
    // status. In this case, default to display the debug_id instead of stack
    // unwind information.
    var legacyRender = isNil_1.default(image.debug_status);
    var debugIdElement = (<ImageSubtext>
        <ImageProp>{locale_1.t('Debug ID')}</ImageProp>: <Formatted>{image.debug_id}</Formatted>
      </ImageSubtext>);
    var formattedImageStartAddress = startAddress ? (<Formatted>{utils_1.formatAddress(startAddress, IMAGE_ADDR_LEN)}</Formatted>) : null;
    var formattedImageEndAddress = endAddress ? (<Formatted>{utils_1.formatAddress(endAddress, IMAGE_ADDR_LEN)}</Formatted>) : null;
    return (<DebugImageItem style={style}>
        <ImageInfoGroup>{renderIconElement()}</ImageInfoGroup>

        <ImageInfoGroup>
          {startAddress && endAddress ? (<React.Fragment>
              {formattedImageStartAddress}
              {' \u2013 '}
              <AddressDivider />
              {formattedImageEndAddress}
            </React.Fragment>) : null}
        </ImageInfoGroup>

        <ImageInfoGroup fullWidth>
          <ImageTitle>
            <tooltip_1.default title={image.code_file}>
              <CodeFile>{codeFile}</CodeFile>
            </tooltip_1.default>
            {showDebugFile && <DebugFile> ({debugFile})</DebugFile>}
          </ImageTitle>

          {legacyRender ? (debugIdElement) : (<StatusLine>
              {renderStatus(locale_1.t('Stack Unwinding'), image.unwind_status)}
              {renderStatus(locale_1.t('Symbolication'), image.debug_status)}
            </StatusLine>)}

          {showDetails && (<React.Fragment>
              {showAvailability && (<ImageSubtext>
                  <ImageProp>{locale_1.t('Availability')}</ImageProp>:
                  <debugFileFeature_1.default feature="symtab" available={image.features.has_symbols}/>
                  <debugFileFeature_1.default feature="debug" available={image.features.has_debug_info}/>
                  <debugFileFeature_1.default feature="unwind" available={image.features.has_unwind_info}/>
                  <debugFileFeature_1.default feature="sources" available={image.features.has_sources}/>
                </ImageSubtext>)}

              {!legacyRender && debugIdElement}

              {showCodeId && (<ImageSubtext>
                  <ImageProp>{locale_1.t('Code ID')}</ImageProp>:{' '}
                  <Formatted>{image.code_id}</Formatted>
                </ImageSubtext>)}

              {!!image.arch && (<ImageSubtext>
                  <ImageProp>{locale_1.t('Architecture')}</ImageProp>: {image.arch}
                </ImageSubtext>)}
            </React.Fragment>)}
        </ImageInfoGroup>

        <access_1.default access={['project:releases']}>
          {function (_a) {
            var hasAccess = _a.hasAccess;
            if (!hasAccess) {
                return null;
            }
            var settingsUrl = getSettingsLink();
            if (!settingsUrl) {
                return null;
            }
            return (<ImageActions>
                <tooltip_1.default title={locale_1.t('Search for debug files in settings')}>
                  <button_1.default size="xsmall" icon={<icons_1.IconSearch size="xs"/>} to={settingsUrl}/>
                </tooltip_1.default>
              </ImageActions>);
        }}
        </access_1.default>
      </DebugImageItem>);
});
exports.default = DebugImage;
var DebugImageItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    position: relative;\n  }\n"], ["\n  font-size: ", ";\n  @media (max-width: ", ") {\n    display: grid;\n    grid-gap: ", ";\n    position: relative;\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(1));
var Formatted = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var ImageInfoGroup = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-left: 1em;\n  flex-grow: ", ";\n\n  &:first-child {\n    @media (min-width: ", ") {\n      margin-left: 0;\n    }\n  }\n"], ["\n  margin-left: 1em;\n  flex-grow: ", ";\n\n  &:first-child {\n    @media (min-width: ", ") {\n      margin-left: 0;\n    }\n  }\n"])), function (p) { return (p.fullWidth ? 1 : null); }, function (p) { return p.theme.breakpoints[0]; });
var ImageActions = styled_1.default(ImageInfoGroup)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    position: absolute;\n    top: 15px;\n    right: 20px;\n  }\n  display: flex;\n  align-items: center;\n"], ["\n  @media (max-width: ", ") {\n    position: absolute;\n    top: 15px;\n    right: 20px;\n  }\n  display: flex;\n  align-items: center;\n"])), function (p) { return p.theme.breakpoints[0]; });
var ImageTitle = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var CodeFile = styled_1.default('span')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var DebugFile = styled_1.default('span')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var ImageSubtext = styled_1.default('div')(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var ImageProp = styled_1.default('span')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
var StatusLine = styled_1.default(ImageSubtext)(templateObject_10 || (templateObject_10 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  @media (max-width: ", ") {\n    display: grid;\n  }\n"], ["\n  display: flex;\n  @media (max-width: ", ") {\n    display: grid;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var AddressDivider = styled_1.default('br')(templateObject_11 || (templateObject_11 = tslib_1.__makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var IconWrapper = styled_1.default('span')(templateObject_12 || (templateObject_12 = tslib_1.__makeTemplateObject(["\n  display: inline-block;\n  margin-top: ", ";\n  height: 16px;\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  display: inline-block;\n  margin-top: ", ";\n  height: 16px;\n\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), space_1.default(0.5), function (p) { return p.theme.breakpoints[0]; }, space_1.default(0.25));
var SymbolicationStatus = styled_1.default('span')(templateObject_13 || (templateObject_13 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n  flex-basis: 0;\n  margin-right: 1em;\n\n  svg {\n    margin-left: 0.66ex;\n  }\n"], ["\n  flex-grow: 1;\n  flex-basis: 0;\n  margin-right: 1em;\n\n  svg {\n    margin-left: 0.66ex;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13;
//# sourceMappingURL=debugImage.jsx.map