(function(){rivets.binders.input={publishes:!0,routine:rivets.binders.value.routine,bind:function(el){return $(el).bind("input.rivets",this.publish)},unbind:function(el){return $(el).unbind("input.rivets")}},rivets.configure({prefix:"rv",adapter:{subscribe:function(obj,keypath,callback){return callback.wrapped=function(m,v){return callback(v)},obj.on("change:"+keypath,callback.wrapped)},unsubscribe:function(obj,keypath,callback){return obj.off("change:"+keypath,callback.wrapped)},read:function(obj,keypath){return"cid"===keypath?obj.cid:obj.get(keypath)},publish:function(obj,keypath,value){return obj.cid?obj.set(keypath,value):obj[keypath]=value}}})}).call(this),function(){var BuilderView,EditFieldView,Formbuilder,FormbuilderCollection,FormbuilderModel,ViewFieldView,_ref,_ref1,_ref2,_ref3,_ref4,__hasProp={}.hasOwnProperty,__extends=function(child,parent){function ctor(){this.constructor=child}for(var key in parent)__hasProp.call(parent,key)&&(child[key]=parent[key]);return ctor.prototype=parent.prototype,child.prototype=new ctor,child.__super__=parent.prototype,child};FormbuilderModel=function(_super){function FormbuilderModel(){return _ref=FormbuilderModel.__super__.constructor.apply(this,arguments)}return __extends(FormbuilderModel,_super),FormbuilderModel.prototype.sync=function(){},FormbuilderModel.prototype.indexInDOM=function(){var $wrapper,_this=this;return $wrapper=$(".fb-field-wrapper").filter(function(_,el){return $(el).data("cid")===_this.cid}),$(".fb-field-wrapper").index($wrapper)},FormbuilderModel.prototype.is_input=function(){return null!=Formbuilder.inputFields[this.get(Formbuilder.options.mappings.FIELD_TYPE)]},FormbuilderModel}(Backbone.DeepModel),FormbuilderCollection=function(_super){function FormbuilderCollection(){return _ref1=FormbuilderCollection.__super__.constructor.apply(this,arguments)}return __extends(FormbuilderCollection,_super),FormbuilderCollection.prototype.initialize=function(){return this.on("add",this.copyCidToModel)},FormbuilderCollection.prototype.model=FormbuilderModel,FormbuilderCollection.prototype.comparator=function(model){return model.indexInDOM()},FormbuilderCollection.prototype.copyCidToModel=function(model){return model.attributes.cid=model.cid},FormbuilderCollection}(Backbone.Collection),ViewFieldView=function(_super){function ViewFieldView(){return _ref2=ViewFieldView.__super__.constructor.apply(this,arguments)}return __extends(ViewFieldView,_super),ViewFieldView.prototype.className="fb-field-wrapper",ViewFieldView.prototype.events={"click .subtemplate-wrapper":"focusEditView","click .js-duplicate":"duplicate","click .js-clear":"clear"},ViewFieldView.prototype.initialize=function(options){return this.parentView=options.parentView,this.listenTo(this.model,"change",this.render),this.listenTo(this.model,"destroy",this.remove)},ViewFieldView.prototype.render=function(){return this.$el.addClass("response-field-"+this.model.get(Formbuilder.options.mappings.FIELD_TYPE)).data("cid",this.model.cid).html(Formbuilder.templates["view/base"+(this.model.is_input()?"":"_non_input")]({rf:this.model})),this},ViewFieldView.prototype.focusEditView=function(){return this.parentView.createAndShowEditView(this.model)},ViewFieldView.prototype.clear=function(e){var cb,x,_this=this;switch(e.preventDefault(),e.stopPropagation(),cb=function(){return _this.parentView.handleFormUpdate(),_this.model.destroy()},x=Formbuilder.options.CLEAR_FIELD_CONFIRM,typeof x){case"string":if(confirm(x))return cb();break;case"function":return x(cb);default:return cb()}},ViewFieldView.prototype.duplicate=function(){var attrs;return attrs=_.clone(this.model.attributes),delete attrs.id,attrs.label+=" Copy",this.parentView.createField(attrs,{position:this.model.indexInDOM()+1})},ViewFieldView}(Backbone.View),EditFieldView=function(_super){function EditFieldView(){return _ref3=EditFieldView.__super__.constructor.apply(this,arguments)}return __extends(EditFieldView,_super),EditFieldView.prototype.className="edit-response-field",EditFieldView.prototype.events={"click .js-add-option":"addOption","click .js-remove-option":"removeOption","click .js-default-updated":"defaultUpdated","input .option-label-input":"forceRender"},EditFieldView.prototype.initialize=function(options){return this.parentView=options.parentView,this.listenTo(this.model,"destroy",this.remove)},EditFieldView.prototype.render=function(){return this.$el.html(Formbuilder.templates["edit/base"+(this.model.is_input()?"":"_non_input")]({rf:this.model})),rivets.bind(this.$el,{model:this.model}),this},EditFieldView.prototype.remove=function(){return this.parentView.editView=void 0,this.parentView.$el.find('[data-target="#addField"]').click(),EditFieldView.__super__.remove.apply(this,arguments)},EditFieldView.prototype.addOption=function(e){var $el,i,newOption,options;return $el=$(e.currentTarget),i=this.$el.find(".option").index($el.closest(".option")),options=this.model.get(Formbuilder.options.mappings.OPTIONS)||[],newOption={label:"",checked:!1},i>-1?options.splice(i+1,0,newOption):options.push(newOption),this.model.set(Formbuilder.options.mappings.OPTIONS,options),this.model.trigger("change:"+Formbuilder.options.mappings.OPTIONS),this.forceRender()},EditFieldView.prototype.removeOption=function(e){var $el,index,options;return $el=$(e.currentTarget),index=this.$el.find(".js-remove-option").index($el),options=this.model.get(Formbuilder.options.mappings.OPTIONS),options.splice(index,1),this.model.set(Formbuilder.options.mappings.OPTIONS,options),this.model.trigger("change:"+Formbuilder.options.mappings.OPTIONS),this.forceRender()},EditFieldView.prototype.defaultUpdated=function(e){var $el;return $el=$(e.currentTarget),"checkboxes"!==this.model.get(Formbuilder.options.mappings.FIELD_TYPE)&&this.$el.find(".js-default-updated").not($el).attr("checked",!1).trigger("change"),this.forceRender()},EditFieldView.prototype.forceRender=function(){return this.model.trigger("change")},EditFieldView}(Backbone.View),BuilderView=function(_super){function BuilderView(){return _ref4=BuilderView.__super__.constructor.apply(this,arguments)}return __extends(BuilderView,_super),BuilderView.prototype.SUBVIEWS=[],BuilderView.prototype.events={"click .js-save-form":"saveForm","click .fb-tabs a":"showTab","click .fb-add-field-types a":"addField","mouseover .fb-add-field-types":"lockLeftWrapper","mouseout .fb-add-field-types":"unlockLeftWrapper"},BuilderView.prototype.initialize=function(options){var selector;return selector=options.selector,this.formBuilder=options.formBuilder,this.bootstrapData=options.bootstrapData,null!=selector&&this.setElement($(selector)),this.collection=new FormbuilderCollection,this.collection.bind("add",this.addOne,this),this.collection.bind("reset",this.reset,this),this.collection.bind("change",this.handleFormUpdate,this),this.collection.bind("destroy add reset",this.hideShowNoResponseFields,this),this.collection.bind("destroy",this.ensureEditViewScrolled,this),this.render(),this.collection.reset(this.bootstrapData),this.bindSaveEvent()},BuilderView.prototype.bindSaveEvent=function(){var _this=this;return this.formSaved=!0,this.saveFormButton=this.$el.find(".js-save-form"),this.saveFormButton.attr("disabled",!0).text(Formbuilder.options.dict.ALL_CHANGES_SAVED),Formbuilder.options.AUTOSAVE&&setInterval(function(){return _this.saveForm.call(_this)},5e3),$(window).bind("beforeunload",function(){return _this.formSaved?void 0:Formbuilder.options.dict.UNSAVED_CHANGES})},BuilderView.prototype.reset=function(){return this.$responseFields.html(""),this.addAll()},BuilderView.prototype.render=function(){var subview,_i,_len,_ref5;for(this.$el.html(Formbuilder.templates.page()),this.$fbLeft=this.$el.find(".fb-left"),this.$responseFields=this.$el.find(".fb-response-fields"),this.bindWindowScrollEvent(),this.hideShowNoResponseFields(),_ref5=this.SUBVIEWS,_i=0,_len=_ref5.length;_len>_i;_i++)subview=_ref5[_i],new subview({parentView:this}).render();return this},BuilderView.prototype.bindWindowScrollEvent=function(){var _this=this;return $(window).on("scroll",function(){var maxMargin,newMargin;if(_this.$fbLeft.data("locked")!==!0)return newMargin=Math.max(0,$(window).scrollTop()-_this.$el.offset().top),maxMargin=_this.$responseFields.height(),_this.$fbLeft.css({"margin-top":Math.min(maxMargin,newMargin)})})},BuilderView.prototype.showTab=function(e){var $el,first_model,target;return $el=$(e.currentTarget),target=$el.data("target"),$el.closest("li").addClass("active").siblings("li").removeClass("active"),$(target).addClass("active").siblings(".fb-tab-pane").removeClass("active"),"#editField"!==target&&this.unlockLeftWrapper(),"#editField"===target&&!this.editView&&(first_model=this.collection.models[0])?this.createAndShowEditView(first_model):void 0},BuilderView.prototype.addOne=function(responseField,_,options){var $replacePosition,view;return view=new ViewFieldView({model:responseField,parentView:this}),null!=options.$replaceEl?options.$replaceEl.replaceWith(view.render().el):null==options.position||-1===options.position?this.$responseFields.append(view.render().el):0===options.position?this.$responseFields.prepend(view.render().el):($replacePosition=this.$responseFields.find(".fb-field-wrapper").eq(options.position))[0]?$replacePosition.before(view.render().el):this.$responseFields.append(view.render().el)},BuilderView.prototype.setSortable=function(){var _this=this;return this.$responseFields.hasClass("ui-sortable")&&this.$responseFields.sortable("destroy"),this.$responseFields.sortable({forcePlaceholderSize:!0,placeholder:"sortable-placeholder",stop:function(e,ui){var rf;return ui.item.data("field-type")&&(rf=_this.collection.create(Formbuilder.helpers.defaultFieldAttrs(ui.item.data("field-type")),{$replaceEl:ui.item}),_this.createAndShowEditView(rf)),_this.handleFormUpdate(),!0},update:function(e,ui){return ui.item.data("field-type")?void 0:_this.ensureEditViewScrolled()}}),this.setDraggable()},BuilderView.prototype.setDraggable=function(){var $addFieldButtons,_this=this;return $addFieldButtons=this.$el.find("[data-field-type]"),$addFieldButtons.draggable({connectToSortable:this.$responseFields,helper:function(){var $helper;return $helper=$("<div class='response-field-draggable-helper' />"),$helper.css({width:_this.$responseFields.width(),height:"80px"}),$helper}})},BuilderView.prototype.addAll=function(){return this.collection.each(this.addOne,this),this.setSortable()},BuilderView.prototype.hideShowNoResponseFields=function(){return this.$el.find(".fb-no-response-fields")[this.collection.length>0?"hide":"show"]()},BuilderView.prototype.addField=function(e){var field_type;return field_type=$(e.currentTarget).data("field-type"),this.createField(Formbuilder.helpers.defaultFieldAttrs(field_type))},BuilderView.prototype.createField=function(attrs,options){var rf;return rf=this.collection.create(attrs,options),this.createAndShowEditView(rf),this.handleFormUpdate()},BuilderView.prototype.createAndShowEditView=function(model){var $newEditEl,$responseFieldEl;if($responseFieldEl=this.$el.find(".fb-field-wrapper").filter(function(){return $(this).data("cid")===model.cid}),$responseFieldEl.addClass("editing").siblings(".fb-field-wrapper").removeClass("editing"),this.editView){if(this.editView.model.cid===model.cid)return this.$el.find('.fb-tabs a[data-target="#editField"]').click(),void this.scrollLeftWrapper($responseFieldEl);this.editView.remove()}return this.editView=new EditFieldView({model:model,parentView:this}),$newEditEl=this.editView.render().$el,this.$el.find(".fb-edit-field-wrapper").html($newEditEl),this.$el.find('.fb-tabs a[data-target="#editField"]').click(),this.scrollLeftWrapper($responseFieldEl),this},BuilderView.prototype.ensureEditViewScrolled=function(){return this.editView?this.scrollLeftWrapper($(".fb-field-wrapper.editing")):void 0},BuilderView.prototype.scrollLeftWrapper=function($responseFieldEl){var _this=this;return this.unlockLeftWrapper(),$responseFieldEl[0]?$.scrollWindowTo(this.$el.offset().top+$responseFieldEl.offset().top-this.$responseFields.offset().top,200,function(){return _this.lockLeftWrapper()}):void 0},BuilderView.prototype.lockLeftWrapper=function(){return this.$fbLeft.data("locked",!0)},BuilderView.prototype.unlockLeftWrapper=function(){return this.$fbLeft.data("locked",!1)},BuilderView.prototype.handleFormUpdate=function(){return this.updatingBatch?void 0:(this.formSaved=!1,this.saveFormButton.removeAttr("disabled").text(Formbuilder.options.dict.SAVE_FORM))},BuilderView.prototype.saveForm=function(){var payload;if(!this.formSaved)return this.formSaved=!0,this.saveFormButton.attr("disabled",!0).text(Formbuilder.options.dict.ALL_CHANGES_SAVED),this.collection.sort(),payload=JSON.stringify({fields:this.collection.toJSON()}),Formbuilder.options.HTTP_ENDPOINT&&this.doAjaxSave(payload),this.formBuilder.trigger("save",payload)},BuilderView.prototype.doAjaxSave=function(payload){var _this=this;return $.ajax({url:Formbuilder.options.HTTP_ENDPOINT,type:Formbuilder.options.HTTP_METHOD,data:payload,contentType:"application/json",success:function(data){var datum,_i,_len,_ref5;for(_this.updatingBatch=!0,_i=0,_len=data.length;_len>_i;_i++)datum=data[_i],null!=(_ref5=_this.collection.get(datum.cid))&&_ref5.set({id:datum.id}),_this.collection.trigger("sync");return _this.updatingBatch=void 0}})},BuilderView}(Backbone.View),Formbuilder=function(){function Formbuilder(opts){var args;null==opts&&(opts={}),_.extend(this,Backbone.Events),args=_.extend(opts,{formBuilder:this}),this.mainView=new BuilderView(args)}return Formbuilder.helpers={defaultFieldAttrs:function(field_type){var attrs,_base;return attrs={},attrs[Formbuilder.options.mappings.LABEL]="Untitled",attrs[Formbuilder.options.mappings.FIELD_TYPE]=field_type,attrs[Formbuilder.options.mappings.REQUIRED]=!1,attrs.field_options={},("function"==typeof(_base=Formbuilder.fields[field_type]).defaultAttributes?_base.defaultAttributes(attrs):void 0)||attrs},simple_format:function(x){return null!=x?x.replace(/\n/g,"<br />"):void 0}},Formbuilder.options={BUTTON_CLASS:"fb-button",HTTP_ENDPOINT:"",HTTP_METHOD:"POST",AUTOSAVE:!0,CLEAR_FIELD_CONFIRM:!1,mappings:{SIZE:"field_options.size",UNITS:"field_options.units",LABEL:"label",FIELD_TYPE:"field_type",REQUIRED:"required",ADMIN_ONLY:"admin_only",OPTIONS:"field_options.options",DESCRIPTION:"field_options.description",INCLUDE_OTHER:"field_options.include_other_option",INCLUDE_BLANK:"field_options.include_blank_option",INTEGER_ONLY:"field_options.integer_only",MIN:"field_options.min",MAX:"field_options.max",MINLENGTH:"field_options.minlength",MAXLENGTH:"field_options.maxlength",LENGTH_UNITS:"field_options.min_max_length_units"},dict:{ALL_CHANGES_SAVED:"All changes saved",SAVE_FORM:"Save form",UNSAVED_CHANGES:"You have unsaved changes. If you leave this page, you will lose those changes!"}},Formbuilder.fields={},Formbuilder.inputFields={},Formbuilder.nonInputFields={},Formbuilder.registerField=function(name,opts){var x,_i,_len,_ref5;for(_ref5=["view","edit"],_i=0,_len=_ref5.length;_len>_i;_i++)x=_ref5[_i],opts[x]=_.template(opts[x]);return opts.field_type=name,Formbuilder.fields[name]=opts,"non_input"===opts.type?Formbuilder.nonInputFields[name]=opts:Formbuilder.inputFields[name]=opts},Formbuilder}(),window.Formbuilder=Formbuilder,"undefined"!=typeof module&&null!==module?module.exports=Formbuilder:window.Formbuilder=Formbuilder}.call(this),function(){Formbuilder.registerField("checkboxes",{order:10,view:"<% for (i in (rf.get(Formbuilder.options.mappings.OPTIONS) || [])) { %>\n  <div>\n    <label class='fb-option'>\n      <input type='checkbox' <%= rf.get(Formbuilder.options.mappings.OPTIONS)[i].checked && 'checked' %> onclick=\"javascript: return false;\" />\n      <%= rf.get(Formbuilder.options.mappings.OPTIONS)[i].label %>\n    </label>\n  </div>\n<% } %>\n\n<% if (rf.get(Formbuilder.options.mappings.INCLUDE_OTHER)) { %>\n  <div class='other-option'>\n    <label class='fb-option'>\n      <input type='checkbox' />\n      Other\n    </label>\n\n    <input type='text' />\n  </div>\n<% } %>",edit:"<%= Formbuilder.templates['edit/options']({ includeOther: true }) %>",addButton:'<span class="symbol"><span class="fa fa-square-o"></span></span> Checkboxes',defaultAttributes:function(attrs){return attrs.field_options.options=[{label:"",checked:!1},{label:"",checked:!1}],attrs}})}.call(this),function(){Formbuilder.registerField("number",{order:30,view:"<input type='text' />\n<% if (units = rf.get(Formbuilder.options.mappings.UNITS)) { %>\n  <%= units %>\n<% } %>",edit:"<%= Formbuilder.templates['edit/min_max']() %>\n<%= Formbuilder.templates['edit/units']() %>\n<%= Formbuilder.templates['edit/integer_only']() %>",addButton:'<span class="symbol"><span class="fa fa-number">123</span></span> Value'})}.call(this),function(){Formbuilder.registerField("radio",{order:15,view:"<% for (i in (rf.get(Formbuilder.options.mappings.OPTIONS) || [])) { %>\n  <div>\n    <label class='fb-option'>\n      <input type='radio' <%= rf.get(Formbuilder.options.mappings.OPTIONS)[i].checked && 'checked' %> onclick=\"javascript: return false;\" />\n      <%= rf.get(Formbuilder.options.mappings.OPTIONS)[i].label %>\n    </label>\n  </div>\n<% } %>\n\n<% if (rf.get(Formbuilder.options.mappings.INCLUDE_OTHER)) { %>\n  <div class='other-option'>\n    <label class='fb-option'>\n      <input type='radio' />\n      Other\n    </label>\n\n    <input type='text' />\n  </div>\n<% } %>",edit:"<%= Formbuilder.templates['edit/options']({ includeOther: true }) %>",addButton:'<span class="symbol"><span class="fa fa-circle-o"></span></span> Single Choice',defaultAttributes:function(attrs){return attrs.field_options.options=[{label:"",checked:!1},{label:"",checked:!1}],attrs}})}.call(this),function(){Formbuilder.registerField("group",{order:100,view:"<label class='section-name'><%= rf.get(Formbuilder.options.mappings.LABEL) %></label>\n<p><%= rf.get(Formbuilder.options.mappings.DESCRIPTION) %></p>",edit:"<div class='fb-edit-section-header'>Label</div>\n<input type='text' data-rv-input='model.<%= Formbuilder.options.mappings.LABEL %>' />\n<textarea data-rv-input='model.<%= Formbuilder.options.mappings.DESCRIPTION %>'\n  placeholder='Add a longer description to this field'></textarea>",addButton:"<span class='symbol'><span class='fa fa-minus'></span></span> Group"})}.call(this),this.Formbuilder=this.Formbuilder||{},this.Formbuilder.templates=this.Formbuilder.templates||{},this.Formbuilder.templates["edit/base"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+=(null==(__t=Formbuilder.templates["edit/base_header"]())?"":__t)+"\n"+(null==(__t=Formbuilder.templates["edit/common"]())?"":__t)+"\n"+(null==(__t=Formbuilder.fields[rf.get(Formbuilder.options.mappings.FIELD_TYPE)].edit({rf:rf}))?"":__t)+"\n";return __p},this.Formbuilder.templates["edit/base_header"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='fb-field-label'>\n  <span data-rv-text=\"model."+(null==(__t=Formbuilder.options.mappings.LABEL)?"":__t)+"\"></span>\n  <code class='field-type' data-rv-text='model."+(null==(__t=Formbuilder.options.mappings.FIELD_TYPE)?"":__t)+"'></code>\n  <span class='fa fa-arrow-right pull-right'></span>\n</div>";return __p},this.Formbuilder.templates["edit/base_non_input"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+=(null==(__t=Formbuilder.templates["edit/base_header"]())?"":__t)+"\n"+(null==(__t=Formbuilder.fields[rf.get(Formbuilder.options.mappings.FIELD_TYPE)].edit({rf:rf}))?"":__t)+"\n";return __p},this.Formbuilder.templates["edit/checkboxes"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<label>\n  <input type='checkbox' data-rv-checked='model."+(null==(__t=Formbuilder.options.mappings.REQUIRED)?"":__t)+"' />\n  Required\n</label>\n<!-- label>\n  <input type='checkbox' data-rv-checked='model."+(null==(__t=Formbuilder.options.mappings.ADMIN_ONLY)?"":__t)+"' />\n  Admin only\n</label -->";return null},this.Formbuilder.templates["edit/common"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='fb-edit-section-header'>Label</div>\n\n<div class='fb-common-wrapper'>\n  <div class='fb-label-description'>\n    "+(null==(__t=Formbuilder.templates["edit/label_description"]())?"":__t)+"\n  </div>\n  <div class='fb-common-checkboxes'>\n    "+(null==(__t=Formbuilder.templates["edit/checkboxes"]())?"":__t)+"\n  </div>\n  <div class='fb-clear'></div>\n</div>\n";return __p},this.Formbuilder.templates["edit/integer_only"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='fb-edit-section-header'>Mark as present if set</div>\n<label>\n  <input type='checkbox' data-rv-checked='model."+(null==(__t=Formbuilder.options.mappings.INTEGER_ONLY)?"":__t)+"' />\n  Mark as present if set\n</label>\n";return __p},this.Formbuilder.templates["edit/label_description"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<input type='text' data-rv-input='model."+(null==(__t=Formbuilder.options.mappings.LABEL)?"":__t)+"' />\n<textarea data-rv-input='model."+(null==(__t=Formbuilder.options.mappings.DESCRIPTION)?"":__t)+"'\n  placeholder='Add a longer description to this field'></textarea>";return __p},this.Formbuilder.templates["edit/min_max"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+='<div class=\'fb-edit-section-header\'>Minimum / Maximum</div>\n\nAbove\n<input type="text" data-rv-input="model.'+(null==(__t=Formbuilder.options.mappings.MIN)?"":__t)+'" style="width: 30px" />\n\n&nbsp;&nbsp;\n\nBelow\n<input type="text" data-rv-input="model.'+(null==(__t=Formbuilder.options.mappings.MAX)?"":__t)+'" style="width: 30px" />\n';return __p},this.Formbuilder.templates["edit/min_max_length"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+='<div class=\'fb-edit-section-header\'>Length Limit</div>\n\nMin\n<input type="text" data-rv-input="model.'+(null==(__t=Formbuilder.options.mappings.MINLENGTH)?"":__t)+'" style="width: 30px" />\n\n&nbsp;&nbsp;\n\nMax\n<input type="text" data-rv-input="model.'+(null==(__t=Formbuilder.options.mappings.MAXLENGTH)?"":__t)+'" style="width: 30px" />\n\n&nbsp;&nbsp;\n\n<select data-rv-value="model.'+(null==(__t=Formbuilder.options.mappings.LENGTH_UNITS)?"":__t)+'" style="width: auto;">\n  <option value="characters">characters</option>\n  <option value="words">words</option>\n</select>\n';return __p},this.Formbuilder.templates["edit/options"]=function(obj){obj||(obj={});{var __t,__p="";_.escape,Array.prototype.join}with(obj)__p+="<div class='fb-edit-section-header'>Options</div>\n\n",__p+="\n\n<div class='option' data-rv-each-option='model."+(null==(__t=Formbuilder.options.mappings.OPTIONS)?"":__t)+'\'>\n  <input type="checkbox" class=\'js-default-updated\' data-rv-checked="option:checked" />\n  <input type="text" data-rv-input="option:label" class=\'option-label-input\' />\n  <a class="js-add-option '+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+'" title="Add Option"><i class=\'fa fa-plus-circle\'></i></a>\n  <a class="js-remove-option '+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+'" title="Remove Option"><i class=\'fa fa-minus-circle\'></i></a>\n</div>\n\n',__p+="\n\n<div class='fb-bottom-add'>\n  <a class=\"js-add-option "+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+'">Add option</a>\n</div>\n';return __p},this.Formbuilder.templates["edit/size"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='fb-edit-section-header'>Size</div>\n<select data-rv-value=\"model."+(null==(__t=Formbuilder.options.mappings.SIZE)?"":__t)+'">\n  <option value="small">Small</option>\n  <option value="medium">Medium</option>\n  <option value="large">Large</option>\n</select>\n';return __p},this.Formbuilder.templates["edit/units"]=function(obj){obj||(obj={});{var __p="";_.escape}return __p},this.Formbuilder.templates.page=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+=(null==(__t=Formbuilder.templates["partials/save_button"]())?"":__t)+"\n"+(null==(__t=Formbuilder.templates["partials/left_side"]())?"":__t)+"\n"+(null==(__t=Formbuilder.templates["partials/right_side"]())?"":__t)+"\n<div class='fb-clear'></div>";return __p},this.Formbuilder.templates["partials/add_field"]=function(obj){obj||(obj={});{var __t,__p="";_.escape,Array.prototype.join}with(obj)__p+="<div class='fb-tab-pane active' id='addField'>\n  <div class='fb-add-field-types'>\n    <div class='section'>\n      ",_.each(_.sortBy(Formbuilder.inputFields,"order"),function(f){__p+='\n        <a data-field-type="'+(null==(__t=f.field_type)?"":__t)+'" class="'+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+'">\n          '+(null==(__t=f.addButton)?"":__t)+"\n        </a>\n      "}),__p+="\n    </div>\n\n    <!--div class='section'>\n      ",_.each(_.sortBy(Formbuilder.nonInputFields,"order"),function(f){__p+='\n        <a data-field-type="'+(null==(__t=f.field_type)?"":__t)+'" class="'+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+'">\n          '+(null==(__t=f.addButton)?"":__t)+"\n        </a>\n      "}),__p+="\n    </div -->\n  </div>\n</div>";return __p},this.Formbuilder.templates["partials/edit_field"]=function(obj){obj||(obj={});{var __p="";_.escape}with(obj)__p+="<div class='fb-tab-pane' id='editField'>\n  <div class='fb-edit-field-wrapper'></div>\n</div>\n";return __p},this.Formbuilder.templates["partials/left_side"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='fb-left'>\n  <ul class='fb-tabs'>\n    <li class='active'><a data-target='#addField'>Add new field</a></li>\n    <li><a data-target='#editField'>Edit field</a></li>\n  </ul>\n\n  <div class='fb-tab-content'>\n    "+(null==(__t=Formbuilder.templates["partials/add_field"]())?"":__t)+"\n    "+(null==(__t=Formbuilder.templates["partials/edit_field"]())?"":__t)+"\n  </div>\n</div>";return __p},this.Formbuilder.templates["partials/right_side"]=function(obj){obj||(obj={});{var __p="";_.escape}with(obj)__p+="<div class='fb-right'>\n  <div class='fb-no-response-fields'>No response fields</div>\n  <div class='fb-response-fields'></div>\n</div>\n";return __p},this.Formbuilder.templates["partials/save_button"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='fb-save-wrapper'>\n  <button class='js-save-form "+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+"'></button>\n</div>";return __p},this.Formbuilder.templates["view/base"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='subtemplate-wrapper'>\n  <div class='cover'></div>\n  "+(null==(__t=Formbuilder.templates["view/label"]({rf:rf}))?"":__t)+"\n\n  "+(null==(__t=Formbuilder.fields[rf.get(Formbuilder.options.mappings.FIELD_TYPE)].view({rf:rf}))?"":__t)+"\n\n  "+(null==(__t=Formbuilder.templates["view/description"]({rf:rf}))?"":__t)+"\n  "+(null==(__t=Formbuilder.templates["view/duplicate_remove"]({rf:rf}))?"":__t)+"\n</div>\n";return __p},this.Formbuilder.templates["view/base_non_input"]=function(obj){obj||(obj={});{var __p="";_.escape}with(obj)__p+="";return __p},this.Formbuilder.templates["view/description"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<span class='help-block'>\n  "+(null==(__t=Formbuilder.helpers.simple_format(rf.get(Formbuilder.options.mappings.DESCRIPTION)))?"":__t)+"\n</span>\n";return __p},this.Formbuilder.templates["view/duplicate_remove"]=function(obj){obj||(obj={});{var __t,__p="";_.escape}with(obj)__p+="<div class='actions-wrapper'>\n  <a class=\"js-duplicate "+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+'" title="Duplicate Field"><i class=\'fa fa-plus-circle\'></i></a>\n  <a class="js-clear '+(null==(__t=Formbuilder.options.BUTTON_CLASS)?"":__t)+'" title="Remove Field"><i class=\'fa fa-minus-circle\'></i></a>\n</div>';return __p},this.Formbuilder.templates["view/label"]=function(obj){obj||(obj={});{var __t,__p="";_.escape,Array.prototype.join}with(obj)__p+="<label>\n  <span>"+(null==(__t=Formbuilder.helpers.simple_format(rf.get(Formbuilder.options.mappings.LABEL)))?"":__t)+"\n  ",rf.get(Formbuilder.options.mappings.REQUIRED)&&(__p+="\n    <abbr title='required'>*</abbr>\n  "),__p+="\n</label>\n";return __p};