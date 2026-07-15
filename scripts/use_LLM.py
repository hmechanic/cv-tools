import os

import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

REQUEST_TIMEOUT = (10, 120)
LATEX_ESCAPE_MAP = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "%": r"\%",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex_text(text):
    """Escape untrusted plain text before inserting it into LaTeX."""
    if not text:
        return text
    return "".join(LATEX_ESCAPE_MAP.get(char, char) for char in text)


def clean_unicode_for_latex(text):
    """
    Clean Unicode characters that cause LaTeX compilation errors.
    Removes or replaces problematic Unicode characters with LaTeX-safe alternatives.
    """
    if not text:
        return text

    # Dictionary of Unicode characters to replace
    unicode_replacements = {
        '\u202f': ' ',  # Narrow no-break space -> regular space
        '\u00a0': ' ',  # No-break space -> regular space
        '\u2013': '--', # En dash -> LaTeX en dash
        '\u2014': '---', # Em dash -> LaTeX em dash
        '\u2018': '`',   # Left single quotation mark -> LaTeX grave accent
        '\u2019': "'",   # Right single quotation mark -> LaTeX apostrophe
        '\u201c': '``',  # Left double quotation mark -> LaTeX quotes
        '\u201d': "''",  # Right double quotation mark -> LaTeX quotes
        '\u2026': '...', # Horizontal ellipsis -> LaTeX ellipsis
        '\u00b0': ' degrees', # Degree symbol -> plain text
        '\u00d7': ' x ',      # Multiplication sign -> plain text
        '\u00f7': '/',        # Division sign -> plain text
        '\u2260': '!=',       # Not equal -> plain text
        '\u2264': '<=',       # Less or equal -> plain text
        '\u2265': '>=',       # Greater or equal -> plain text
    }

    # Replace known problematic Unicode characters
    for unicode_char, latex_equivalent in unicode_replacements.items():
        text = text.replace(unicode_char, latex_equivalent)

    # Remove any remaining non-ASCII characters that might cause issues
    # Keep only printable ASCII characters and common Latin-1 characters
    cleaned_text = ''
    for char in text:
        # Keep ASCII printable characters and common accented characters
        if ord(char) < 128 or (192 <= ord(char) <= 255):
            cleaned_text += char
        else:
            # Replace unknown Unicode with space or remove
            cleaned_text += ' '

    # Clean up multiple spaces
    import re
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

def generate_prompt(config, long_profile, job_offer, language='es'):

    if language == 'es':
        prompt = f"""
            # MISION
            Actuarás como un estratega de talento y redactor experto de CVs. Tu misión es construir un perfil profesional de alto impacto, personalizado para la oferta de trabajo adjunta, utilizando únicamente la información proporcionada sobre mí.

            # CONTEXTO
            Para esta tarea, te proporciono tres documentos. La hoja de vida es la fuente principal de verdad. El perfil extendido ofrece contexto adicional.

            <documento_1: MI_HOJA_DE_VIDA>
            {config}
            </documento_1: MI_HOJA_DE_VIDA>

            <documento_2: PERFIL_EXTENDIDO>
            {long_profile}
            </documento_2: PERFIL_EXTENDIDO>

            <documento_3: OFERTA_DE_TRABAJO>
            {job_offer}
            </documento_3: OFERTA_DE_TRABAJO>

            # PLAN DE EJECUCIÓN
            Sigue estos pasos rigurosamente:

            1.  **Fase de Análisis (Pensamiento Interno):**
                *   **Paso 1.1:** Deconstruye la <OFERTA_DE_TRABAJO>. Identifica y extrae las 3 a 5 competencias, habilidades técnicas y requisitos más críticos. Busca palabras clave específicas del rol o la industria.
                *   **Paso 1.2:** Revisa mi <MI_HOJA_DE_VIDA> y el <PERFIL_EXTENDIDO> para encontrar evidencia directa y logros que demuestren mi capacidad en las áreas clave identificadas en el paso anterior. Prioriza siempre los logros cuantificables (con números, porcentajes o métricas).

            2.  **Fase de Redacción (Generación de Salida):**
                *   **Paso 2.1:** Redacta el perfil en primera persona (ej: "Soy ingeniero...", "He liderado proyectos...").
                *   **Paso 2.2:** Estructura el resultado en exactamente dos párrafos de texto continuo, sin usar viñetas ni listas.
                *   **Paso 2.3 (Primer Párrafo):** Comienza con una declaración de impacto. Menciona mis años de experiencia, mi especialización principal y cómo esta se alinea directamente con el puesto ofertado. Integra de forma fluida y natural las palabras clave más importantes de la oferta.
                *   **Paso 2.4 (Segundo Párrafo):** Presenta 2 o 3 de mis logros más relevantes o habilidades específicas que respondan directamente a los requisitos más importantes de la oferta. Utiliza verbos de acción potentes (ej: "optimicé", "implementé", "lideré") y enfócate en los resultados cuantificables que encontraste en la fase de análisis.

            # REGLAS Y RESTRICCIONES
            *   **Adherencia Estricta:** No inventes, infieras ni añadas información que no esté explícitamente en la hoja de vida o la descripción larga solo para ajustarse perfectamente a la oferta.
            *   **Formato de Salida:** La salida final debe ser únicamente el texto de los dos párrafos del perfil profesional. No incluyas saludos, explicaciones, títulos ni ningún otro texto introductorio.
            *   **Tono:** El lenguaje debe ser profesional, seguro, conciso y orientado a resultados.
            *   **Longitud:** La respuesta completa no debe exceder los 1000 caracteres.
        """

    elif language == 'en':
        prompt = f"""
            # MISSION
            You will act as a talent strategist and expert resume writer. Your mission is to craft a high-impact, professional profile tailored specifically to the attached job offer, using only the information I provide.

            # CONTEXT
            For this task, I am providing you with three documents. The resume is the primary source of truth. The extended profile offers additional context.

            <document_1: MY_RESUME>
            {config}
            </document_1: MY_RESUME>

            <document_2: EXTENDED_PROFILE>
            {long_profile}
            </document_2: EXTENDED_PROFILE>

            <document_3: JOB_OFFER>
            {job_offer}
            </document_3: JOB_OFFER>

            # EXECUTION PLAN
            Follow these steps rigorously:

            1.  **Analysis Phase (Internal Thought Process):**
                *   **Step 1.1:** Deconstruct the <JOB_OFFER>. Identify and extract the 3 to 5 most critical competencies, technical skills, and requirements. Look for specific keywords relevant to the role or industry.
                *   **Step 1.2:** Review my <MY_RESUME> and <EXTENDED_PROFILE> to find direct evidence and achievements that demonstrate my capabilities in the key areas identified in the previous step. Always prioritize quantifiable achievements (with numbers, percentages, or metrics).

            2.  **Writing Phase (Output Generation):**
                *   **Step 2.1:** Write the profile in the first person (e.g., "I am an engineer...", "I have led projects...").
                *   **Step 2.2:** Structure the output into exactly two paragraphs of continuous text, without using bullet points or lists.
                *   **Step 2.3 (First Paragraph):** Start with an impact statement. Mention my years of experience, my main area of specialization, and how it directly aligns with the offered position. Seamlessly and naturally integrate the most important keywords from the job offer.
                *   **Step 2.4 (Second Paragraph):** Showcase 2-3 of my most relevant achievements or specific skills that directly address the most critical requirements of the offer. Use powerful action verbs (e.g., "optimized," "implemented," "led") and focus on the quantifiable results you found during the analysis phase.

            # RULES AND CONSTRAINTS
            *   **Strict Adherence:** Do not invent, infer, or add any information that is not explicitly stated in the provided documents.
            *   **Output Format:** The final output must be only the text of the two-paragraph professional profile. Do not include greetings, explanations, titles, or any other introductory text.
            *   **Tone:** The language must be professional, confident, concise, and results-oriented.
            *   **Length:** The entire response must not exceed 1000 characters.
        """
    print("Generated prompt for LLM:")
    print(prompt)
    return prompt


def get_ai_response(query, model_name='openai/gpt-oss-120b', max_tokens=10000, temp=0.1):
    """
    Send a query to the selected LLM API (Groq or OpenRouter) and get a response.
    """

    api_provider = os.getenv("API_PROVIDER", "groq").lower()

    if api_provider == "groq":
        print("Using Groq API...")
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY is not configured")
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                temperature=temp,
                max_completion_tokens=max_tokens,
                top_p=0.9,
                reasoning_effort="medium",
                stop=None
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return f"Failed to get response: {str(e)}"

    elif api_provider == "openrouter":
        print("Using OpenRouter API...")
        try:
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY is not configured")
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ],
                    "temperature": temp,
                    "max_tokens": max_tokens,
                    "top_p": 0.8
                },
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return f"Failed to get response: {str(e)}"

    return "Failed to get response: API_PROVIDER must be 'groq' or 'openrouter'"

def generate_professional_profile(config, job_offer_path):
    """Generate a professional profile using LLM."""

    try:
        with open(job_offer_path, "r") as file:
            job_offer = file.read()

    except FileNotFoundError:
        print("Error: Job offer file not found!")
        return ""

    try:
        with open("config/longProfile.txt", "r") as file:
            long_profile_content = file.read()
    except FileNotFoundError:
        print("Error: longProfile.txt not found!")
        return ""

    language = config['heading']["language"]
    if language == 'es':
        long_profile = long_profile_content.split("=== Professional Profile (English) ===")[0].strip()
    else:
        long_profile = long_profile_content.split("=== Professional Profile (English) ===")[1].strip()

    query = generate_prompt(config, long_profile, job_offer, language=language)

    print("Generating professional profile with LLM...")
    profile = get_ai_response(query)
    print("Done")

    # Clean Unicode characters that cause LaTeX errors
    profile = escape_latex_text(clean_unicode_for_latex(profile))
    return profile


def generate_experience_bullets(config, job_offer_path, section_name, original_bullets):
    """Generate enhanced experience bullets tailored to job offer."""

    if not original_bullets:
        return original_bullets

    try:
        with open(job_offer_path, "r") as file:
            job_offer = file.read()
    except FileNotFoundError:
        print("Error: Job offer file not found!")
        return original_bullets

    enhanced_bullets = []

    # Extract skills from CV config
    skills_text = ""
    for section in config.get('sections', []):
        if section.get('type') == 'skills':
            for skill_group in section.get('content', []):
                for entity in skill_group.get('entity', []):
                    skills_text += f"{entity.get('name', '')}: {entity.get('data', '')}\n"

    for bullet in original_bullets:
        prompt = f"""
            # EXPERIENCE BULLET ENHANCEMENT

            JOB REQUIREMENTS: {job_offer[:500]}...

            MY SKILLS FROM CV: {skills_text.strip()}

            ORIGINAL BULLET: "{bullet}"

            TASK: Rewrite this bullet to:
            1. Emphasize skills matching the job requirements (ONLY use skills listed in "MY SKILLS FROM CV" above)
            2. Add quantifiable achievements where possible (e.g., percentages, numbers)
            3. Integrate relevant keywords naturally
            4. Maintain professional, action-oriented language
            5. Keep under 150 characters

            IMPORTANT RESTRICTIONS:
            - Only reference skills that are explicitly listed in "MY SKILLS FROM CV"
            - Do not invent or add skills that aren't in the original CV
            - If no matching skills exist, focus on experience alignment with job requirements
            - Do not invent information. If no quantifiable data exists, focus on skills alignment.

            Tone and Style:

                * Professional and confident
                * Natural, fluid, and concise writing.
                * Avoid clichés, filler phrases, and generic wording.

            ENHANCED BULLET:
        """

        print(f"Enhancing bullet: {bullet[:50]}...")
        enhanced = get_ai_response(prompt)
        if enhanced and not enhanced.startswith("Failed"):
            # Clean Unicode characters that cause LaTeX errors
            enhanced = escape_latex_text(clean_unicode_for_latex(enhanced.strip()))
            enhanced_bullets.append(enhanced)
        else:
            print("Enhancement failed, using original bullet.")
            enhanced_bullets.append(bullet)  # Fallback to original

    return enhanced_bullets

